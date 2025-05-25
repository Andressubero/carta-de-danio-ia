import uuid
from sqlalchemy import Column, String, Integer, Boolean, Date, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import date
import enum

Base = declarative_base()

# Tipo UUID compatible con múltiples bases de datos
class GUID(TypeDecorator):
    impl = CHAR
    cache_ok = True
    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            return str(uuid.UUID(value))
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return uuid.UUID(value)

# Enum para tipo de daño
class DamageTypeEnum(str, enum.Enum):
    ABOLLADURA = "ABOLLADURA"
    RALLON = "RALLON"
    OTRO = "OTRO"
    SIN_DANO = "SIN_DANO"

class ImageTypeEnum(str, enum.Enum):
    LATERAL_RIGHT = "image_lateral_right"
    LATERAL_LEFT = "image_lateral_left"
    FRONT = "image_front"
    BACK = "image_back"
    TOP = "image_top"


class VehicleTypePart(Base):
    __tablename__ = 'vehicle_type_part'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    vehicle_type_id = Column(GUID(), ForeignKey('vehicle_type.id'))
    part_id = Column(GUID(), ForeignKey('part.id'))

class Role(Base):
    __tablename__ = 'role'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))

class User(Base):
    __tablename__ = 'user'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True)
    email = Column(String(255))
    password = Column(String(255))
    role_id = Column(GUID(), ForeignKey('role.id'))

    role = relationship("Role")
    vehicles = relationship("Vehicle", back_populates="owner")

class VehicleType(Base):
    __tablename__ = 'vehicle_type'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))

    parts = relationship("VehicleTypePart", backref="vehicle_type")

class Part(Base):
    __tablename__ = 'part'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    image_type = Column(Enum(ImageTypeEnum), nullable=False)

    vehicle_types = relationship("VehicleTypePart", backref="part")

class Vehicle(Base):
    __tablename__ = 'vehicle'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey('user.id'))
    vehicle_type_id = Column(GUID(), ForeignKey('vehicle_type.id'))
    model = Column(String(255))
    brand = Column(String(255))
    year = Column(Integer)
    plate = Column(String(255), unique=True)

    owner = relationship("User", back_populates="vehicles")
    type = relationship("VehicleType")
    states = relationship("VehicleState", back_populates="vehicle")

class VehicleState(Base):
    __tablename__ = 'vehicle_state'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(GUID(), ForeignKey('vehicle.id'))
    date = Column(Date, default=date.today)
    validation_reasons = Column(String(255), nullable=True)

    vehicle = relationship("Vehicle", back_populates="states")
    parts_state = relationship("VehiclePartState", back_populates="vehicle_state")

class VehiclePart(Base):
    __tablename__ = 'vehicle_part'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    vehicle_id = Column(GUID(), ForeignKey('vehicle.id'))
    part_id = Column(GUID(), ForeignKey('part.id'))

    vehicle = relationship("Vehicle")
    part = relationship("Part")
    part_states = relationship("VehiclePartState", back_populates="vehicle_part")

class Image(Base):
    __tablename__ = 'images'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    url = Column(String(255), nullable=False)

    # Opcional: si querés la relación inversa
    vehicle_part_states = relationship("VehiclePartState", back_populates="image")


class VehiclePartState(Base):
    __tablename__ = 'vehicle_part_state'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    vehicle_state_id = Column(GUID(), ForeignKey('vehicle_state.id'))
    vehicle_part_id = Column(GUID(), ForeignKey('vehicle_part.id'))
    image_id = Column(GUID(), ForeignKey('images.id')) 

    vehicle_state = relationship("VehicleState", back_populates="parts_state")
    vehicle_part = relationship("VehiclePart", back_populates="part_states")
    damages = relationship("Damage", back_populates="vehicle_part_state")
    image = relationship("Image", back_populates="vehicle_part_states")

class Damage(Base):
    __tablename__ = 'damage'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    vehicle_part_state_id = Column(GUID(), ForeignKey('vehicle_part_state.id'))
    damage_type = Column(Enum(DamageTypeEnum))
    description = Column(String(255))
    fixed = Column(Boolean, default=False)

    vehicle_part_state = relationship("VehiclePartState", back_populates="damages")
