from datetime import datetime, timezone
import pandas as pd
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from logger import LOGGER

from src.database import session, stack_optimizer_session
from src.repository.models import Appointment, ContainerInformation, OptimizationSummary, OptimizationDetail, OptimizationMove
from src.util.config_loader import Config
from src.stackoptimizer.main_so import main_so
from src.util.simulate_data import generate_bays_data


def run_optimization(input_params):
    """

    :return: appointments
    """
    optimization_summary_id = input_params['optimizationSummaryId']
    location_uuid = input_params['locationUUID']
    if "simulate" not in input_params:
        simulate = False  
    else:
        simulate =  input_params['simulate']



    try:
        if simulate:
            containers_location_appointment_df = generate_bays_data()
            data_info = "Data simulated"
            print(data_info)
        else:

            result = session.query(Appointment).join(ContainerInformation,
                                                        Appointment.pickup_container_id == ContainerInformation.id).filter(
                ContainerInformation.container_location_row.isnot(None),
                ContainerInformation.container_location_tier.isnot(None),
                ContainerInformation.container_location_slot.isnot(None),
                # ContainerInformation.container_location_stack.isnot(None),
                Appointment.appointment_location_uuid == location_uuid,
                Appointment.appointment_start_time > '2023-10-05').all()

            LOGGER.success(f"retrieved appointments")
            container_for_optimizer_list = []

            for row in result:

                container_for_optimizer = {
                    "container_location_bay": row.pickup_container.container_location_row,
                    "container_location_tier": row.pickup_container.container_location_tier,
                    "container_location_stack": row.pickup_container.container_location_slot,
                    "container_location_block": row.pickup_container.container_location_stack,
                    "appointment_start_time": row.appointment_start_time,
                    "appointment_end_time": row.appointment_end_time,
                    "container_id": row.pickup_container.container_id
                }
                container_for_optimizer_list.append(container_for_optimizer)
            containers_location_appointment_df =pd.DataFrame(container_for_optimizer_list)
            containers_location_appointment_df['container_location_block'] = containers_location_appointment_df['container_location_block'].fillna("R")
            for col in ['container_location_bay','container_location_tier','container_location_stack']:
                containers_location_appointment_df[col] = containers_location_appointment_df[col].astype(int)

            data_info = "Data extracted from SQLDB"
            print(data_info)

        block_config_df = pd.DataFrame.from_dict({'container_location_block':["R"],'stacks_per_bay':[5],'tiers_per_bay':[5]})
        filepath = Config.value('root_folder')+Config.value('folderpath')

        print(containers_location_appointment_df.head())
        print(block_config_df.head())

        # WRITE INPUT
        containers_location_appointment_df.to_csv(filepath + str(optimization_summary_id)+ "_input_containers_location_appointment_df.csv")
        block_config_df.to_csv(filepath+ str(optimization_summary_id) + "_input_block_config_df.csv")

        output = main_so(containers_location_appointment_df,block_config_df,plot_filepath=filepath+ str(optimization_summary_id) + "_output.pdf")
        container_summary_data = output[0]
        work_orders = output[1]

        # WRITE OUTPUT
        container_summary_data.to_csv(filepath+ str(optimization_summary_id) +"_output_container_summary_data.csv")
        work_orders.to_csv(filepath+ str(optimization_summary_id) +"_output_work_orders.csv")

        upload_data_to_sqldb(optimization_summary_id,container_summary_data)
        # upload_data_to_sql_workorder(optimization_summary_id, work_orders)

        output_msg = data_info + " & Output is saved on GCP"
        return output_msg



    except IntegrityError as e:
        LOGGER.error(f"IntegrityError when creating user: {e}")
    except SQLAlchemyError as e:
        LOGGER.error(f"SQLAlchemyError when creating user: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when creating user: {e}")
    except Exception as e:
        print(e)
    finally:
        stack_optimizer_session.close()


def save_optimization_run_details(data):

    optimization_summary = stack_optimizer_session.query(OptimizationSummary).get(data["optimization_summary_id"])
    optimization_summary.status = "COMPLETED"
    optimization_summary.end_datetime = datetime.now(timezone.utc)
    optimization_summary.number_of_containers = 1
    optimization_summary.number_of_workorders = 2
    optimization_summary.number_of_reshuffles = 2

    optimization_detail = OptimizationDetail(
        optimization_summary_id = data["optimization_summary_id"],
        current_block = data["current_block"],
        current_bay = data["current_bay"],
        new_block = data["new_block"],
        new_bay = data["new_bay"],
        container_id=data["container_id"],
        current_stack=data["current_stack"],
        current_tier=data["current_tier"],
        new_stack=data["new_stack"],
        new_tier=data["new_tier"],
        created_by = "py",
        modified_by = "py",
        created_on = datetime.now(timezone.utc),
        modified_on = datetime.now(timezone.utc),
    )

    optimization_summary.optimization_details.append(optimization_detail)


def save_optimization_moves(data):
    optimization_summary = stack_optimizer_session.query(OptimizationSummary).get(data["optimization_summary_id"])
    optimization_move = OptimizationMove(
        optimization_summary_id = data["optimization_summary_id"],
        workorder = data["work_order"],
        block = data["block"],
        bay = data["bay"],
        move_sequence = data["move_sequence"],
        expected_relocation_moves = data["calculated_erms"],
        created_by = "py",
        modified_by = "py",
        created_on = datetime.now(timezone.utc),
        modified_on = datetime.now(timezone.utc),
    )
    optimization_summary.optimization_moves.append(optimization_move)

def upload_data_to_sqldb(optimization_summary_id,data):
    data["optimization_summary_id"] = optimization_summary_id
    data.apply(save_optimization_run_details,axis=1)
    stack_optimizer_session.commit()

def upload_data_to_sql_workorder(optimization_summary_id,data):
    data["optimization_summary_id"] = optimization_summary_id
    data.apply(save_optimization_moves,axis=1)
    stack_optimizer_session.commit()