import uuid
from sqlalchemy import Column, String, Integer, Boolean, Date, Enum, ForeignKey, Table, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import date, datetime
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
    ROTURA = "ROTURA"
    
class ValidationStateEnum(str, enum.Enum):
    PENDING = "PENDIENTE"
    APPROVED = "APROBADA"
    DENIED = "DENEGADA"

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
    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "role": self.role.name if self.role else None
        }

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
    parts = relationship("VehiclePart", back_populates="vehicle", cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "vehicle_type_id": str(self.vehicle_type_id),
            "model": self.model,
            "brand": self.brand,
            "year": self.year,
            "plate": self.plate,
            "type": self.type.name if self.type else None,
            "parts": [
                        {
                            "id": str(part.id),
                            "name": part.name
                        }
                        for part in self.parts
                    ]
        }

class VehicleState(Base):
    __tablename__ = 'vehicle_state'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(GUID(), ForeignKey('vehicle.id'))
    creation_date = Column(DateTime, default=datetime.utcnow)
    validation_reasons = Column(Text, nullable=True)
    declared_date = Column(Date, default=date.today)
    validation_state = Column(Enum(ValidationStateEnum), default = ValidationStateEnum.PENDING)
    vehicle = relationship("Vehicle", back_populates="states")
    parts_state = relationship("VehiclePartState", back_populates="vehicle_state")
    ai_reports = relationship("AIReport", back_populates="vehicle_state", cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "id": str(self.id),
            "vehicle_id": str(self.vehicle_id),
            "vehicle_brand": self.vehicle.brand if self.vehicle else None,
            "vehicle_model": self.vehicle.model if self.vehicle else None,
            "creation_date": self.creation_date.isoformat(),
            "validation_reasons": self.validation_reasons,
            "declared_date": self.declared_date.isoformat() if self.declared_date else None,
            "validation_state": self.validation_state.value,  
            "parts_state": [part.to_dict() for part in self.parts_state]
        }


    
    
    

class VehiclePart(Base):
    __tablename__ = 'vehicle_part'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    vehicle_id = Column(GUID(), ForeignKey('vehicle.id'))
    part_id = Column(GUID(), ForeignKey('part.id'))

    vehicle = relationship("Vehicle", back_populates="parts")
    part = relationship("Part")
    part_states = relationship("VehiclePartState", back_populates="vehicle_part")



class VehiclePartState(Base):
    __tablename__ = 'vehicle_part_state'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    vehicle_state_id = Column(GUID(), ForeignKey('vehicle_state.id'))
    vehicle_part_id = Column(GUID(), ForeignKey('vehicle_part.id'))
    image = Column(String(255), nullable=True)
    creation_date = Column(DateTime, default=datetime.utcnow)

    vehicle_state = relationship("VehicleState", back_populates="parts_state")
    vehicle_part = relationship("VehiclePart", back_populates="part_states")
    damages = relationship("Damage", back_populates="vehicle_part_state")
    def to_dict(self):
        return {
            "id": str(self.id),
            "vehicle_part_id": str(self.vehicle_part_id),
            "vehicle_part_name": self.vehicle_part.name if self.vehicle_part else None,
            "image": self.image,
            "creation_date": self.creation_date.isoformat(),
            "damages": [damage.to_dict() for damage in self.damages]
        }

class Damage(Base):
    __tablename__ = 'damage'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    vehicle_part_state_id = Column(GUID(), ForeignKey('vehicle_part_state.id'))
    damage_type = Column(Enum(DamageTypeEnum))
    description = Column(String(255))
    fixed = Column(Boolean, default=False)

    vehicle_part_state = relationship("VehiclePartState", back_populates="damages")
    def to_dict(self):
        return {
            "id": str(self.id),
            "damage_type": self.damage_type.value,
            "description": self.description,
            "fixed": self.fixed
        }

class AIReport(Base):
    __tablename__ = 'ai_report'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)

    vehicle_state_id = Column(GUID(), ForeignKey('vehicle_state.id'), nullable=False)
    vehicle_state = relationship("VehicleState", back_populates="ai_reports")

    is_vehicle_valid = Column(Boolean, nullable=False)
    image_type = Column(String(100))
    vehicle_type = Column(String(100))
    estimated_brand = Column(String(255))
    estimated_model = Column(String(255))
    image_quality = Column(String(50))
    is_same_unit_as_reference = Column(Boolean)
    same_unit_confidence = Column(Integer)  # 0 to 100
    total_vehicle_damage_percentage = Column(String(10))
    additional_comments = Column(Text)
    comparison_with_reference = Column(Text)
    validation_reasons = Column(Text)

    # Relación a daños por parte
    part_damages = relationship(
        "AIReportPartDamage",
        back_populates="ai_report",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": str(self.id),
            "vehicle_state_id": str(self.vehicle_state_id),
            "is_vehicle_valid": self.is_vehicle_valid,
            "image_type": self.image_type,
            "vehicle_type": self.vehicle_type,
            "estimated_brand": self.estimated_brand,
            "estimated_model": self.estimated_model,
            "image_quality": self.image_quality,
            "is_same_unit_as_reference": self.is_same_unit_as_reference,
            "same_unit_confidence": self.same_unit_confidence,
            "total_vehicle_damage_percentage": self.total_vehicle_damage_percentage,
            "additional_comments": self.additional_comments,
            "comparison_with_reference": self.comparison_with_reference,
            "validation_reasons": self.validation_reasons,
            "part_damages": [damage.to_dict() for damage in self.part_damages]
        }


class AIReportPartDamage(Base):
    __tablename__ = 'ai_report_part_damage'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    ai_report_id = Column(GUID(), ForeignKey('ai_report.id'), nullable=False)
    ai_report = relationship("AIReport", back_populates="part_damages")

    part_name = Column(String(255))
    severity = Column(String(50))  # LOW, MID, HIGH
    damage_type = Column(String(100))
    damage_description = Column(Text)
    confidence_percentage = Column(Integer)
    present_in_reference = Column(Boolean, nullable=True)  # en AIReport sin referencia puede quedar en null

    def to_dict(self):
        return {
            "id": str(self.id),
            "ai_report_id": str(self.ai_report_id),
            "part_name": self.part_name,
            "severity": self.severity,
            "damage_type": self.damage_type,
            "damage_description": self.damage_description,
            "confidence_percentage": self.confidence_percentage,
            "present_in_reference": self.present_in_reference
        }
