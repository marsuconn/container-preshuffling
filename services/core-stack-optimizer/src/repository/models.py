from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Index, Integer, JSON, SmallInteger, String, TIMESTAMP, \
    text, MetaData
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from src.database import engine, session, stack_optimizer_engine, stack_optimizer_session
from dataclasses import dataclass
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, SQLAlchemyAutoSchema

mymetadata = MetaData()
Base = declarative_base(metadata=mymetadata)


class ApiLog(Base):
    __tablename__ = 'api_log'

    id = Column(BigInteger, primary_key=True)
    message = Column(LONGTEXT)
    url = Column(String(2500))
    headers = Column(String(1000))
    params = Column(String(1000))
    status = Column(Integer)
    generatedId = Column(String(36), nullable=False)
    type = Column(String(45))
    message_type = Column(String(45))
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)


class AppointmentParameter(Base):
    __tablename__ = 'appointment_parameter'

    id = Column(BigInteger, primary_key=True)
    appointment_location_uuid = Column(String(50))
    org_code = Column(String(45))
    parameter_name = Column(String(100), nullable=False)
    parameter_value = Column(String(100))
    parameter_category = Column(String(100))
    value_type = Column(String(100))
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)


class AuditLog(Base):
    __tablename__ = 'audit_log'

    id = Column(BigInteger, primary_key=True)
    entity_id = Column(BigInteger, nullable=False)
    entity_name = Column(String(100), nullable=False)
    trace_id = Column(String(100))
    change_log = Column(JSON)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)


class CapacityCriterion(Base):
    __tablename__ = 'capacity_criteria'

    id = Column(BigInteger, primary_key=True)
    criteria_name = Column(String(100), nullable=False)
    criteria_type = Column(String(20), nullable=False)
    organization = Column(String(45), nullable=False)
    appointment_location_uuid = Column(String(50), index=True)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)


class CapacityUtilizationHistory(Base):
    __tablename__ = 'capacity_utilization_history'
    __table_args__ = (
        Index('index_appointment_location_uuid_start_of_day', 'appointment_location_uuid', 'start_of_day'),
    )

    id = Column(BigInteger, primary_key=True)
    appointment_location_uuid = Column(String(50), nullable=False)
    organization = Column(String(45), nullable=False)
    start_of_day = Column(DateTime, nullable=False)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)


class ContainerInformation(Base):
    __tablename__ = 'container_information'
    __table_args__ = (
        Index('index_container_id_type_org', 'container_id', 'container_type', 'organization'),
    )

    id = Column(BigInteger, primary_key=True)
    container_id = Column(String(200), nullable=False, index=True)
    check_digit = Column(String(200))
    appointment_location_name = Column(String(200))
    appointment_location_uuid = Column(String(50))
    organization = Column(String(45), nullable=False)
    ready_for_drop_off = Column(TINYINT(1), server_default=text("'0'"))
    ready_for_pickup = Column(TINYINT(1), server_default=text("'0'"))
    ready_for_pickup_datetime = Column(DateTime)
    container_location = Column(String(200))
    last_free_date = Column(DateTime)
    scheduled_eta = Column(DateTime)
    has_way_bill = Column(TINYINT(1), server_default=text("'0'"))
    holds = Column(TINYINT(1), server_default=text("'0'"))
    storage_fee_paid = Column(TINYINT(1), server_default=text("'0'"))
    rail_cutoff = Column(DateTime)
    active = Column(TINYINT(1), server_default=text("'1'"))
    appointment_id = Column(BigInteger, index=True)
    customer_id = Column(String(200))
    chassis_number = Column(String(200))
    container_location_stack = Column(String(200))
    container_location_row = Column(String(200))
    container_location_tier = Column(String(200))
    container_location_slot = Column(String(200))
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)
    pickup_number = Column(String(200))
    operating_station_code = Column(String(200))
    container_type = Column(String(20), nullable=False)
    message = Column(LONGTEXT)
    gate_restrictions = Column(LONGTEXT)
    reject_reason_code = Column(String(100))
    location_timezone = Column(String(50), nullable=False)


class ContainerReference(Base):
    __tablename__ = 'container_reference'

    id = Column(BigInteger, primary_key=True)
    appointment_id = Column(BigInteger, index=True)
    container_watchlist_id = Column(BigInteger, index=True)
    workorder = Column(String(100))
    shipment = Column(String(100))
    receiver_code = Column(String(100))
    stop_number = Column(Integer)
    originator_code = Column(String(100))
    originator_name = Column(String(100))
    receiver_name = Column(String(100))
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)


class Customer(Base):
    __tablename__ = 'customer'
    __table_args__ = (
        Index('index_customer_id_organization', 'customer_id', 'organization'),
        Index('index_organization_active', 'organization', 'active')
    )

    id = Column(BigInteger, primary_key=True)
    customer_id = Column(String(200), nullable=False)
    short_name = Column(String(50), nullable=False)
    long_name = Column(String(200), nullable=False)
    organization = Column(String(45), nullable=False)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)
    active = Column(TINYINT(1), server_default=text("'1'"))


class FlywaySchemaHistory(Base):
    __tablename__ = 'flyway_schema_history'

    installed_rank = Column(Integer, primary_key=True)
    version = Column(String(50))
    description = Column(String(200), nullable=False)
    type = Column(String(20), nullable=False)
    script = Column(String(1000), nullable=False)
    checksum = Column(Integer)
    installed_by = Column(String(100), nullable=False)
    installed_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    execution_time = Column(Integer, nullable=False)
    success = Column(TINYINT(1), nullable=False, index=True)


class Rule(Base):
    __tablename__ = 'rule'
    __table_args__ = (
        Index('index_appointment_location_uuid_name', 'appointment_location_uuid', 'name'),
    )

    id = Column(BigInteger, primary_key=True)
    name = Column(String(200), nullable=False)
    appointment_location_uuid = Column(String(50))
    grace_period = Column(BigInteger, nullable=False)
    organization = Column(String(45), nullable=False)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)
    enabled = Column(TINYINT(1), server_default=text("'1'"))


class Template(Base):
    __tablename__ = 'template'

    id = Column(BigInteger, primary_key=True)
    template_name = Column(String(100), nullable=False)
    organization = Column(String(45), nullable=False)
    appointment_location_uuid = Column(String(50), index=True)
    working_hours_start_hour = Column(Integer, nullable=False)
    working_hours_start_minute = Column(Integer, nullable=False)
    working_hours_end_hour = Column(Integer, nullable=False)
    working_hours_end_minute = Column(Integer, nullable=False)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)
    template_description = Column(String(100))


class UnsubscribedUser(Base):
    __tablename__ = 'unsubscribed_user'

    id = Column(BigInteger, primary_key=True)
    email = Column(String(400), nullable=False, unique=True)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)


class Utilization(Base):
    __tablename__ = 'utilization'
    __table_args__ = (
        Index('index_location_start_time_end_time_criteria_id', 'appointment_location_uuid', 'start_time', 'end_time',
              'capacity_criteria_id'),
    )

    id = Column(BigInteger, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity_criteria_id = Column(BigInteger, nullable=False)
    organization = Column(String(45), nullable=False)
    appointment_location_uuid = Column(String(50))
    booked_count = Column(Integer, nullable=False)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)


@dataclass
class Appointment(Base):
    __tablename__ = 'appointment'
    __table_args__ = (
        Index('index_created_by_start_time', 'created_by', 'appointment_start_time'),
    )

    id = Column(BigInteger, primary_key=True)
    organization = Column(String(45))
    appointment_location_uuid = Column(String(50), nullable=False, index=True)
    appointment_type = Column(String(100), nullable=False)
    appointment_start_time = Column(DateTime, nullable=False)
    appointment_end_time = Column(DateTime, nullable=False)
    pickup_container_id = Column(ForeignKey('container_information.id'), index=True)
    drop_container_id = Column(ForeignKey('container_information.id'), index=True)
    pickup_container_reference = Column(ForeignKey('container_reference.id'), index=True)
    drop_container_reference = Column(ForeignKey('container_reference.id'), index=True)
    status = Column(String(20), nullable=False)
    gate_in_time = Column(DateTime)
    gate_out_time = Column(DateTime)
    cancel_reason_code = Column(String(100))
    cancel_reason = Column(String(1000))
    appointment_originator_code = Column(String(20))
    notification_email = Column(String(200))
    pickup_number = Column(String(20))
    hotload = Column(TINYINT(1), server_default=text("'0'"))
    driver_license = Column(String(50))
    driver_name = Column(String(100))
    driver_state = Column(String(100))
    driver_country = Column(String(100))
    scac = Column(String(100))
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)
    appointment_number = Column(String(30), nullable=False, unique=True)
    comments = Column(LONGTEXT)
    location_timezone = Column(String(50), nullable=False)
    workorder = Column(String(100))
    shipment = Column(String(100))
    receiver_code = Column(String(100))
    stop_number = Column(Integer)
    appointment_originator_name = Column(String(100))
    receiver_name = Column(String(100))
    cancelled_by = Column(String(100))
    driver_ssoid = Column(String(100))
    appointment_location = Column(String(200))
    cancelled_date = Column(DateTime)
    driver_email = Column(String(200))
    created_by_sso = Column(TINYINT(1), server_default=text("'0'"))

    drop_container = relationship('ContainerInformation',
                                  primaryjoin='Appointment.drop_container_id == ContainerInformation.id')
    container_reference = relationship('ContainerReference',
                                       primaryjoin='Appointment.drop_container_reference == ContainerReference.id')
    pickup_container = relationship('ContainerInformation',
                                    primaryjoin='Appointment.pickup_container_id == ContainerInformation.id')
    container_reference1 = relationship('ContainerReference',
                                        primaryjoin='Appointment.pickup_container_reference == ContainerReference.id')


class ContainerWatchlist(Base):
    __tablename__ = 'container_watchlist'
    __table_args__ = (
        Index('index_container_id_org', 'pickup_container_id', 'organization'),
        Index('index_created_by_container_id_location_pickup_number', 'created_by', 'pickup_container_id',
              'appointment_location_uuid', 'pickup_number')
    )

    id = Column(BigInteger, primary_key=True)
    pickup_container_id = Column(String(45))
    pickup_check_digit = Column(String(200))
    organization = Column(String(45), nullable=False)
    appointment_location_uuid = Column(String(200), nullable=False)
    pickup_number = Column(String(200))
    appointment_ready = Column(String(20))
    originator_code = Column(String(200))
    notification_email = Column(String(200))
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)
    scheduled_eta = Column(DateTime)
    last_free_date = Column(DateTime)
    message = Column(LONGTEXT)
    appointment_type = Column(String(45))
    drop_container_id = Column(String(45))
    drop_check_digit = Column(String(45))
    pickup_reject_reason_code = Column(String(100))
    location_timezone = Column(String(50), nullable=False)
    pickup_container_reference = Column(ForeignKey('container_reference.id'), index=True)
    drop_container_reference = Column(ForeignKey('container_reference.id'), index=True)
    workorder = Column(String(100))
    shipment = Column(String(100))
    receiver_code = Column(String(100))
    stop_number = Column(Integer)
    scac = Column(String(100))
    drop_reject_reason_code = Column(String(100))
    originator_name = Column(String(100))
    receiver_name = Column(String(100))
    is_eligible_for_auto_appointment = Column(TINYINT(1), server_default=text("'0'"))
    driver_email = Column(String(200))
    created_by_sso = Column(TINYINT(1), server_default=text("'0'"))

    container_reference = relationship('ContainerReference',
                                       primaryjoin='ContainerWatchlist.drop_container_reference == ContainerReference.id')
    container_reference1 = relationship('ContainerReference',
                                        primaryjoin='ContainerWatchlist.pickup_container_reference == ContainerReference.id')


class CriteriaCondition(Base):
    __tablename__ = 'criteria_conditions'

    id = Column(BigInteger, primary_key=True)
    capacity_criteria_id = Column(ForeignKey('capacity_criteria.id'), nullable=False, index=True)
    attribute_name = Column(String(100), nullable=False)
    attribute_value = Column(String(100), nullable=False)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

    capacity_criteria = relationship('CapacityCriterion')


class CriteriaOfTheDay(Base):
    __tablename__ = 'criteria_of_the_day'

    id = Column(BigInteger, primary_key=True)
    capacity_utilization_history_id = Column(ForeignKey('capacity_utilization_history.id'), index=True)
    capacity_criteria_id = Column(BigInteger)
    capacity_criteria_name = Column(String(100))
    criteria_type = Column(String(100))
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

    capacity_utilization_history = relationship('CapacityUtilizationHistory')


class CriteriaTiming(Base):
    __tablename__ = 'criteria_timings'

    id = Column(BigInteger, primary_key=True)
    capacity_criteria_id = Column(ForeignKey('capacity_criteria.id'), nullable=False, index=True)
    start_time_hour = Column(SmallInteger)
    start_time_minute = Column(SmallInteger)
    end_time_hour = Column(SmallInteger)
    end_time_minute = Column(SmallInteger)
    day_of_week = Column(String(45), nullable=False)
    limit = Column(Integer)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

    capacity_criteria = relationship('CapacityCriterion')


class TemplateApplicability(Base):
    __tablename__ = 'template_applicability'
    __table_args__ = (
        Index('index_location_exception', 'appointment_location_uuid', 'exception'),
    )

    id = Column(BigInteger, primary_key=True)
    organization = Column(String(45), nullable=False)
    appointment_location_uuid = Column(String(50))
    date_range_start = Column(DateTime, nullable=False)
    date_range_end = Column(DateTime, nullable=False)
    exception = Column(TINYINT(1), server_default=text("'0'"))
    template_id = Column(ForeignKey('template.id'), nullable=False, index=True)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)
    active = Column(TINYINT(1), server_default=text("'1'"))

    template = relationship('Template')


class TemplateCapacityCriterion(Base):
    __tablename__ = 'template_capacity_criteria'

    id = Column(BigInteger, primary_key=True)
    template_id = Column(ForeignKey('template.id'), nullable=False, index=True)
    capacity_criteria_id = Column(ForeignKey('capacity_criteria.id'), nullable=False, index=True)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

    capacity_criteria = relationship('CapacityCriterion')
    template = relationship('Template')


class TimeCapacityUtilizationHistory(Base):
    __tablename__ = 'time_capacity_utilization_history'

    id = Column(BigInteger, primary_key=True)
    capacity_utilization_history_id = Column(ForeignKey('capacity_utilization_history.id'), index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity_criteria_id = Column(BigInteger)
    limit = Column(Integer)
    utilization_id = Column(BigInteger)
    booked_count = Column(Integer)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

    capacity_utilization_history = relationship('CapacityUtilizationHistory')


class CriteriaConditionOfTheDay(Base):
    __tablename__ = 'criteria_condition_of_the_day'

    id = Column(BigInteger, primary_key=True)
    criteria_of_the_day_id = Column(ForeignKey('criteria_of_the_day.id'), index=True)
    attribute_name = Column(String(100))
    attribute_value = Column(String(100))
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

    criteria_of_the_day = relationship('CriteriaOfTheDay')


class UtilizationAppointment(Base):
    __tablename__ = 'utilization_appointments'

    id = Column(BigInteger, primary_key=True)
    utilization_id = Column(ForeignKey('utilization.id'), nullable=False, index=True)
    appointment_id = Column(ForeignKey('appointment.id'), nullable=False, index=True)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

    appointment = relationship('Appointment')
    utilization = relationship('Utilization')


Base.metadata.create_all(engine)


class AppointmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        load_instance = True
        sqla_session = session


appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)


class OptimizationSummary(Base):
    __tablename__ = 'optimization_summary'

    id = Column(BigInteger, primary_key=True)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    status = Column(String(20))
    number_of_containers = Column(BigInteger)
    number_of_workorders = Column(BigInteger)
    number_of_reshuffles = Column(BigInteger)
    location_uuid = Column(String(50))
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

    optimization_details = relationship("OptimizationDetail", back_populates="optimization_summary")
    optimization_moves = relationship("OptimizationMove", back_populates="optimization_summary")


class OptimizationDetail(Base):
    __tablename__ = 'optimization_detail'

    id = Column(BigInteger, primary_key=True)
    optimization_summary_id = Column(ForeignKey('optimization_summary.id'), index=True)
    container_id = Column(String(50), nullable=False)
    current_block = Column(String(50), nullable=False)
    current_bay = Column(String(50), nullable=False)
    current_stack = Column(String(50), nullable=False)
    current_tier = Column(String(50), nullable=False)
    new_block = Column(String(50), nullable=False)
    new_bay = Column(String(50), nullable=False)
    new_stack = Column(String(50), nullable=False)
    new_tier = Column(String(50), nullable=False)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

    optimization_summary = relationship("OptimizationSummary", back_populates="optimization_details")


class OptimizationMove(Base):
    __tablename__ = 'optimization_move'

    id = Column(BigInteger, primary_key=True)
    optimization_summary_id = Column(ForeignKey('optimization_summary.id'), index=True)
    workorder = Column(String(50), nullable=False)
    block = Column(String(50))
    bay = Column(String(50))
    move_sequence = Column(String(500), nullable=False)
    expected_relocation_moves = Column(BigInteger, nullable=False)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

    optimization_summary = relationship("OptimizationSummary", back_populates="optimization_moves")

