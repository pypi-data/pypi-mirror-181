"""THIS CODE IS A WORK IN PROGRESS"""
import collections
import inspect
import logging
import typing
from datetime import datetime

import attr
import coloring
import sqlalchemy
from koalak.consts import PACKAGE_NAME
from koalak.decorators import add_post_init, optionalargs
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger("koalak")
logger.setLevel(logging.DEBUG)

try:
    typping_ForwardRef = typing.ForwardRef
except AttributeError:
    typping_ForwardRef = typing._ForwardRef  # noqa


class ProgrammingError(Exception):
    """Things that should not happen!"""

    pass


"""
RelationalDB is a wrapper for sqlalchemy and attr to have
a relational database with a better API and abstraction
- no ID
- specify relations with annoation (List["Animal"], Animal, ...)
- use attr to create __init__, __repr__, ...
See examples in test_relationaldb.py



"""

"""
TODO: Error tests
- Default None -> Nullable True
- Not null and default is None => error
-
"""
AttribType = type(attr.ib())
AttrNOTHING = attr.ib()._default


def parse_typing_type(t):
    if len(t.__args__) != 1:
        raise ValueError("Annotation list must have one and only one argument")

    return {"type": t._name, "name": t.__args__[0].__forward_arg__}


@attr.s
class ColumnMetadata:
    """Helper cls to build relational attribute"""

    name: str = attr.ib()
    type = attr.ib(kw_only=True, default=None)
    many: bool = attr.ib(default=None)
    referenced_by: "ColumnMetadata" = attr.ib(default=None)
    attr_attribute = attr.ib(default=None)
    unique = attr.ib(default=None)
    nullable = attr.ib(default=None)
    default = attr.ib(default=None)

    # this attribute is set to True by the class that contain this
    #  attribute, sins it is possible for an other class to create
    #  an attribute with ref (having exist=True we are sure that
    #  the attribute exist and it's not just a reference)
    exist = attr.ib(default=None)

    def update(
        self,
        *,
        many=None,
        type=None,
        referenced_by=None,
        attr_attribute=None,
        exist=None,
        unique=None,
        nullable=None,
        default=None,
    ):
        for varname in [
            "exist",
            "many",
            "type",
            "unique",
            "referenced_by",
            "attr_attribute",
            "nullable",
            "default",
        ]:

            var = locals()[varname]
            if var is not None:
                attr = getattr(self, varname)
                if attr is not None:
                    # attr not None and var not None! they must be the same
                    if var is not attr:
                        raise ValueError(
                            f"Trying to update {varname} but it's already set to {attr} "
                        )
                else:
                    setattr(self, varname, var)

    def print(self):
        print_str = f"\t{self.name}: "
        if self.many:
            print_str += "List["
        print_str += f"{self.type}"
        if self.many:
            print_str += "]"

        if self.unique:
            print_str += " [unique]"
        if self.nullable:
            print_str += " [nullable]"
        if self.referenced_by:
            print_str += f" [{self.referenced_by}]"
        if self.exist:
            print_str += " [exists]"
        coloring.print_bblue_violet(print_str)


@attr.s
class TableMetadata:
    """Helper class to postpone building the ORM classes
    Contains all information about a table (name, indexes, ..., ...)"""

    # cls_name is the only information that we always know
    #   either we have it before decorating with @db.table
    #   or it's name is referenced as an annotation in a column
    cls_name: str = attr.ib()
    table_name: str = attr.ib(default=None)  # tablename
    cls = attr.ib(default=None, init=False)
    columns: typing.Dict[str, ColumnMetadata] = attr.ib(factory=dict, init=False)
    orm_cls = attr.ib(default=None, init=False)
    # this attribute is set to True by the class that contain this
    #  attribute, sins it is possible for an other class to create
    #  an attribute with ref (having exist=True we are sure that
    #  the attribute exist and it's not just a reference)
    exist = attr.ib(default=None)

    def update(self, *, cls=None, table_name=None, orm_cls=None, exist=None):
        for varname in ["cls", "table_name", "orm_cls", "exist"]:
            var = locals()[varname]
            if var is not None:
                attr = getattr(self, varname)
                if attr is not None:
                    # attr not None and var not None! they must be the same
                    if var is not attr:
                        raise ValueError(
                            f"Trying to update {varname} but it's already set to {attr} "
                        )
                else:
                    setattr(self, varname, var)

    def print(self):
        coloring.print_bblue(f"Table: {self.table_name} - {self.cls_name}")
        for column in self.columns.values():
            column.print()

    def get_or_create_column(self, attribute_name: str) -> ColumnMetadata:
        if attribute_name in self.columns:
            return self.columns[attribute_name]
        else:
            attribute = ColumnMetadata(attribute_name)
            self.columns[attribute_name] = attribute
            return attribute


class RelationalDB:
    # TODO: add a new engine which is dict in contrast to SQLalchemy
    # it will have the same API, but it will store the classes
    # in memory with list and dicts and don't use SQL
    # TODO: add bijection argument (for friends, to add the same line twice)
    # TODO: add List of strings List[str] => and add a table with a foreign key
    #   Ex: tags: List[str]  -> create table users_tags id_tag
    # TODO: use only annotation without db.attribute(): Ex: name: str  (like dataclass)
    # TODO: add the possibility ti use @db.table  and take the name cls.__name__
    # TODO: implement  lazy import
    _map_cls_to_sqlalchemy_types = {
        str: sqlalchemy.String,
        int: sqlalchemy.Integer,
        bool: sqlalchemy.Boolean,
        datetime: sqlalchemy.DateTime,
    }
    List = typing.List

    def __init__(self, uri: str = None, echo=None, autocommit=None):
        """
        RelationalDB is an aditional layer of abstration for relationaldb ORMs
        This class is based on SQLAlchemy and attrs modules

        Algorithm:
            - Gather information for tables (table) and columns (attributes)
              - add hook in init for each table/class to be able to autocommit
            - call init() to built SQLAlchemy classes based on the gathered information

        Global constraints:
            - Mapped classes (with tables) must have unique names
        """
        if uri is None:
            uri = ":memory:"

        if echo is None:
            echo = False

        if autocommit is None:
            autocommit = True

        self.uri = uri
        self.autocommit = autocommit
        self.debug = echo

        # internal attributes
        # FIXME: remove one of the three mapping
        self._map_cls_tablename = {}
        self._map_tablename_cls = {}

        # sqlalchemy attributes
        self.engine = create_engine(f"sqlite:///{uri}", echo=echo)
        self.Session = sessionmaker(bind=self.engine)
        self.Base = declarative_base()

        # dictionary to hold classes to build at init()
        self._clsname_to_table_metadata: typing.Dict[str, TableMetadata] = {}

    @property
    def query(self):
        return self.session.query

    @property
    def commit(self):
        return self.session.commit

    datetime_now = datetime.utcnow

    def metadata(self, unique=None, nullable=None, target=None, ref=None):
        if unique is None:
            unique = False

        if nullable is None:
            nullable = False

        return {
            "koalak": {
                "unique": unique,
                "nullable": nullable,
                "target": target,
                "ref": ref,
            }
        }

    def attribute(
        self,
        # attrs attribute
        type=None,
        *,
        default=attr.NOTHING,
        validator=None,
        repr=True,
        cmp=None,
        hash=None,
        init=True,
        metadata=None,
        converter=None,
        factory=None,
        kw_only=False,
        eq=None,
        order=None,
        on_setattr=None,
        # sqlalchemy attribute
        unique=None,
        nullable=None,
        target=None,
        ref=None,
    ):

        # check integrity of arguments

        if not nullable and default is None:
            assert TypeError(
                f"An attribute can't be 'not nullable' and default is None in the same time"
            )

        # if default is None activate nullable to True by default
        if default is None and nullable is None:
            nullable = True

        if metadata is None:
            metadata = {}
        if nullable is None:
            nullable = False
        metadata.update(
            self.metadata(unique=unique, target=target, nullable=nullable, ref=ref)
        )
        attrib = attr.ib(  # noqa
            default=default,
            validator=validator,
            repr=repr,
            cmp=cmp,
            hash=hash,
            init=init,
            metadata=metadata,
            type=type,
            converter=converter,
            factory=factory,
            kw_only=kw_only,
            eq=eq,
            order=order,
            on_setattr=on_setattr,
        )
        self.log(f"\tParsing attrib {attrib}")
        coloring.print_red("metadata", attrib.metadata)
        return attrib

    def log(self, *args, **kwargs):
        if self.debug:
            print("[DEBUG]", *args, **kwargs)

    def table(self, table_name):
        """Create new table

        Algorithm:
        This will only add metadata to create the table at init()
        - Decorate the cls with attr module to create the used methods (__init__, __repr__, ...)
        - Hook the __init__ for autocommit (so the class will add itself to session)
        - collect all needed information for relations (to add in init())
        - Create the sqlalchemy ORM cls that inherit from the original cls and the Base cls
         without the relations (relations will be added in init())
        - Return the ORM cls
        """
        self.log(f"Creating table {table_name}")
        self.print()

        def decorator(cls):
            """Register this class to build it when init() is called"""
            # This code is executed after attr.ib and db.attribute constructions
            # check if cls name is unique
            cls_name = cls.__name__
            table_metadata = self._get_or_create_table_metadata_by_clsname(cls_name)
            table_metadata.update(table_name=table_name, cls=cls)

            # TODO: check if cls exists
            # if cls_name in self._clsname_to_table_metadata:
            #    assert KeyError(f"Table with cls name {cls_name} already exists")

            # ======================================= #
            # decorate cls with attr (if not already) #
            # ======================================= #
            if not hasattr(cls, "__attrs_attrs__"):
                # If columns are created with attr.ib and not db.attribute we add koalak metadata
                # We have to create it here, before attr.s parse the attr.ib instances
                for e in cls.__dict__.values():
                    if not isinstance(e, AttribType):
                        continue
                    if "koalak" not in e.metadata:
                        e.metadata["koalak"] = self.metadata()["koalak"]
                    # FIXME: check if attr.ib and db.attribute are coherant

                # Apply attr
                cls = attr.s(cls)
            else:
                raise ValueError(
                    f"Class {cls.__name__} must not be decorated with attr.s use db.table instead!"
                )

            # ========================================== #
            # hook __init__ to add autocommit if enabled #
            # ========================================== #
            def postinit_autocommit(self_instance):
                if self.autocommit:
                    self.session.add(self_instance)
                    # self.session.commit()

            # add postinit_autocommit to the cls
            cls = add_post_init(postinit_autocommit)(cls)

            # register cls and it's attributes
            # orm_cls = self._create_orm_cls_without_relations(cls, table_name)
            self._add_table_metadata(cls, table_name)
            # building_cls = self._register_cls(cls, table_name)

            return cls

        return decorator

    def print(self):
        print("<----------BEGIN-------->")
        for table in self._clsname_to_table_metadata.values():
            table.print()
            print()
        print("<----------END-------->")

    def _get_or_create_table_metadata_by_clsname(self, cls_name: str) -> TableMetadata:
        if cls_name in self._clsname_to_table_metadata:
            return self._clsname_to_table_metadata[cls_name]
        else:
            table_metadata = TableMetadata(cls_name)
            self._clsname_to_table_metadata[cls_name] = table_metadata
            return table_metadata

    def _add_table_metadata(self, cls, table_name):
        """Create the ORM cls without relations. Relations will be added when init() is called"""

        # get the building_class for this class
        cls_name = cls.__name__
        table_metadata = self._get_or_create_table_metadata_by_clsname(cls_name)
        table_metadata.update(exist=True)

        columns_metadata = table_metadata.columns
        attr_attributes = getattr(cls, "__attrs_attrs__")
        """sqlalchemy_attributes = {
            "__tablename__": table_name,
            # Automatically add id
            "id": Column(Integer, primary_key=True),
        }"""

        for attr_attribute in attr_attributes:
            metadata = attr_attribute.metadata["koalak"]
            if attr_attribute.default is None:
                pass
            coloring.print_green("attr", attr_attribute)
            attribute_name = attr_attribute.name

            column_metadata = table_metadata.get_or_create_column(attribute_name)

            column_metadata.update(
                unique=metadata["unique"], nullable=metadata["nullable"]
            )
            # Get sqlalchemy column type
            attr_type = attr_attribute.type
            """
            We can have the following types:
            - Simple types (builtin)
                - SQLAlchemy cls -> do nothing
                - Known builtin type (int, float, bool, str, datetime) -> convert to SQLAlchemy cls
            - Complicated types (relationship with other tables)
                - Cls already present in our tables (cls already decorated with @db.table)
                - Str -> convert it to cls in our table
                - List["str"] or List[cls], many relation with the cls
            - Else error!
            """
            self.print()

            if isinstance(attr_type, type(sqlalchemy.String)):
                # sqlalchemy type (Integer, String, ...)
                column_metadata.update(type=attr_type, many=False)
            elif attr_type in self._map_cls_to_sqlalchemy_types:
                # convert builtin types  (int, str, bool, ...)
                sqlalchemy_type = self._map_cls_to_sqlalchemy_types[attr_attribute.type]
                column_metadata.update(type=attr_type, many=False)
            elif isinstance(attr_type, (str, type(typing.List))) or (
                isinstance(attr_type, type)
                and attr_type.__name__ in self._clsname_to_table_metadata
            ):
                # Complicated type implying relations (one to many, many to many, one to one, ...)
                self._add_relational_column(table_metadata, attr_attribute)

                # check it cls type is the same as this cls
                # if so, nullable must be True! (otherwise it's impossible to instantiate the object)
                # TODO: move the check in _register_building_attribute?
                """if clsname_type == cls.__name__:
                    if not metadata["nullable"]:
                        # TODO: test this case (tell Yassmine?)
                        raise ValueError(
                            f"Attribute {attr_attribute.name!r} must be nullable when "
                            f"it's type is referencing to the same class ({cls.__name__!r})"
                        )
                continue"""
            else:
                raise TypeError(f"Unknown type for attribute {attr_type}")

            # table_metadata.get_or_create_column("")
            # Build kwargs
            # kwargs["unique"] = metadata["unique"]
            # kwargs["nullable"] = metadata["nullable"]
            # Create the Column
            # sqlalchemy_attributes[attribute_name] = Column(
            #     sqlalchemy_type, *args, **kwargs
        #  )

        # sqlalchemy_attributes.update(sqlalchemy_attributes_later)
        # ORM cls inherit from the decorated cls and self.Base
        # OrmCls = type(cls.__name__, (cls, self.Base), sqlalchemy_attributes)
        # ============================================================= #
        # Create a new cls that inherit from Base and the decorated cls #
        # ============================================================= #
        # self._map_tablename_cls[table_name] = OrmCls
        # self._map_cls_tablename[OrmCls] = table_name

        # table_metadata.update(orm_cls=OrmCls)
        # return OrmCls

    def _add_relational_column(
        self, table_metadata: TableMetadata, attr_attribute
    ) -> ColumnMetadata:
        """Register a relational attribute (str or isinstance(type(List)) or cls"""
        coloring.print_green(
            "Adding relational attribute",
            repr(table_metadata.table_name),
            attr_attribute,
        )
        column_name = attr_attribute.name
        attr_type = attr_attribute.type

        # If it's a known Column class, get its name
        if (
            isinstance(attr_type, type)
            and attr_type.__name__ in self._clsname_to_table_metadata
        ):
            attr_type = attr_type.__name__

        metadata = attr_attribute.metadata["koalak"]

        cls = table_metadata.cls
        cls_name = cls.__name__
        column_metadata = table_metadata.get_or_create_column(column_name)
        column_metadata.update(attr_attribute=attr_attribute)
        column_metadata.update(exist=True)
        # check if the attribute is typing.List to use a "many" relationship

        many = False
        if isinstance(attr_type, type(typing.List)):
            parsed_type = parse_typing_type(attr_type)
            attr_type_type = parsed_type["type"]
            if attr_type_type != "List":
                raise ValueError(
                    f"Support only List annotation, don't support {attr_type}"
                )

            many = True
            attr_type = parsed_type["name"]  # noqa

        atomic_type = attr_type
        print("whoop", column_metadata)
        column_metadata.print()
        column_metadata.update(many=many, type=attr_type)
        column_metadata.print()
        # build the ref_type if it doesn't exist
        ref_cls_name = atomic_type
        ref_building_cls = self._get_or_create_table_metadata_by_clsname(atomic_type)

        # check if the attribute have a reference to an other one
        ref_attribute_name = metadata["ref"]
        if ref_attribute_name:
            # check: if the ref_class is already parsed check if ref attribute exist
            if ref_building_cls.exist:
                # if ref_attribute_name not in
                if (
                    ref_attribute_name not in ref_building_cls.columns
                    or not ref_building_cls.columns[ref_attribute_name].exist
                ):
                    raise ValueError(
                        f"{table_metadata.table_name}.{column_name} reference non existing attribute {ref_attribute_name}"
                    )

            # get the building_attribute
            ref_building_attributes = ref_building_cls.columns
            building_attribute_ref = ref_building_cls.get_or_create_column(
                ref_attribute_name
            )

            building_attribute_ref.update(type=cls_name)
            building_attribute_ref.update(referenced_by=column_metadata)

            # Check if reference are consistent
            if building_attribute_ref.referenced_by:
                # check that class is consistent
                #  ex: If Person have an attributes List[Animal] animals, ref=owner
                #  owner must be of type Person!
                ref_attomic_type = building_attribute_ref.type
                if ref_attomic_type and ref_attomic_type != cls_name:
                    raise ValueError(
                        f"{cls_name}.{column_name} reference {ref_cls_name}.{ref_attribute_name}, but "
                        f" {ref_cls_name}.{ref_attribute_name} reference {ref_attomic_type} class"
                    )
                ref_referenced_by_name = building_attribute_ref.referenced_by.name

                if ref_referenced_by_name != column_name:
                    raise ValueError(
                        f"The {cls_name}.{column_name} reference {ref_cls_name}.{ref_attribute_name}"
                        f" but {ref_cls_name}.{ref_attribute_name} "
                        f"reference {cls_name}.{ref_referenced_by_name}"
                    )

        return column_metadata

    def init(self):

        self.print()
        # Check classes!
        for table_metadata in self._clsname_to_table_metadata.values():
            for column_metadata in table_metadata.columns.values():
                for attribute_name in ["many", "unique", "nullable", "type"]:
                    attribute_value = getattr(column_metadata, attribute_name)
                    if attribute_value is None:
                        raise ProgrammingError(
                            f"In column {table_metadata.table_name}.{column_metadata.name}"
                            f" attribute {attribute_name!r} is None"
                        )

        # construict classes
        for cls_name in self._clsname_to_table_metadata:
            self._build_orm_relations(cls_name)

        self.Base.metadata.create_all(self.engine)
        self.session = self.Session()

    def _build_orm_relations(self, cls_name: str):
        buildingn_cls = self._clsname_to_table_metadata[cls_name]
        cls = buildingn_cls.cls
        orm_cls = buildingn_cls.orm_cls
        for building_attribute in buildingn_cls.columns.values():
            # Check if the attribute exist or if it's referenced but don't exist
            if not building_attribute.exist:
                referenced_by = building_attribute.referenced_by
                assert ValueError(
                    f"Attribute {building_attribute.name} is referenced by {referenced_by.name} but don't exist"
                )
            attr_attribute = building_attribute.attr_attribute
            metadata = attr_attribute.metadata["koalak"]
            ref = metadata["ref"]
            many = building_attribute.many
            if not ref:
                ref_many = True
            else:
                ref_many = True

            if not isinstance(building_attribute.type, str):
                ref_type = building_attribute.type._name
            else:
                ref_type = building_attribute.type
            ref_building_cls = self._clsname_to_table_metadata[ref_type]
            if not many and ref_many:
                # one to many relations
                self._build_one_to_many_relation(
                    buildingn_cls, ref_building_cls, building_attribute.name
                )

    def _build_one_to_many_relation(
        self,
        one_cls: TableMetadata,
        many_cls: TableMetadata,
        one_attribute_name,
        one_relation=True,
    ):
        # add the foreign_key in the one_cls side

        many_cls_id = f"{many_cls.table_name}.id"

        foreign_key = Column(Integer, ForeignKey(many_cls_id))
        foreign_key_name = f"{one_attribute_name}_id"
        setattr(one_cls.orm_cls, foreign_key_name, foreign_key)

        if one_relation:

            relation = sqlalchemy.orm.relationship(
                many_cls.name,
                remote_side=many_cls.orm_cls.id,
                foreign_keys=f"{one_cls.name}.{foreign_key_name}",
            )
            setattr(one_cls.orm_cls, one_attribute_name, relation)

    def first(self, table, **kwargs):
        if isinstance(table, str):
            table = self._map_tablename_cls[table]
        return self.session.query(table).filter_by(**kwargs).first()

    def close(self):
        self.commit()

    # aliases
    ib = attribute

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()


def relationaldb(
    uri: str = None, *, debug: bool = None, autocommit: bool = None
) -> RelationalDB:
    return RelationalDB(uri, echo=debug, autocommit=autocommit)
