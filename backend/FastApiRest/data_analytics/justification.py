from db_access.application import get_relevant_application_data
from model.data import EventAnomalyJustifications, JustificationData

ram_relevancy_threshold = 0.05  # percentual threshold applications should have to be considered relevant
cpu_relevancy_threshold = 0.05  # percentual threshold applications should have to be considered relevant


class ApplicationStat:  # class to store application data
    def __init__(self, ram: int, cpu: int, process_change: int):
        self.ram = ram
        self.cpu = cpu
        self.process_change = process_change  # same as event_headers (processes in applications were closed or opened marked with -1, 0 or 1)


def justify_pc_data_points(pc_total_df, significant_data_points: list, pc_id: int):
    """
    Function to loop through event list to call gather_event_logs()

    How event log detection works:
    On init, make a map of applications, if any applications are added/removed later it will be registered
    :return:
    """
    justification_logs = []
    for timestamp in significant_data_points:
        # TODO: coming up with something when theres no data to look back to
        # TODO: coming up with something when there are time gaps between data
        # TODO: only register relevant changes as justification not list everything that happened in important appplications
        total_ram = pc_total_df.loc[pc_total_df['measurement_time'] == timestamp, 'ram'].iloc[0]
        applications_df, application_data_list = get_relevant_application_data(pc_id, timestamp, 5, total_ram*ram_relevancy_threshold, cpu_relevancy_threshold)
        applications_dict = dict()
        print(applications_df)
        for index, row in applications_df.iterrows():
            application_stat = ApplicationStat(
                ram=row['ram'],
                cpu=row['cpu'],
                process_change=row['process_count_difference']
            )
            applications_dict[row['measurement_time']] = {row['name']: application_stat}
        lj = EventAnomalyJustifications(
            timestamp=timestamp,
            justification_list=[]
        )
        justify_data_point(lj, applications_dict)
        justification_logs.append(lj)
    print(justification_logs)
    return justification_logs


def justify_data_point(lj: EventAnomalyJustifications, applications_dict):
    """
    Function to gather information on why an event was caused like an application closing, processes closing or similiar
    :return:
    """
    last_application_dict = None
    for timestamp, application_dict in applications_dict.items():  # looping through our Map<timestamp, Map<name, values>
        for name, data in application_dict.items():  # looping through our Map<name, values>
            if last_application_dict:
                started = False
                stopped = False
                process_change = 0
                delta_ram = 0
                delta_cpu = 0
                warning = False

                if name not in last_application_dict:  # application was started
                    started = True
                    delta_ram = data.ram
                    delta_cpu = data.cpu
                elif name in last_application_dict and name not in last_application_dict:  # application was stopped
                    stopped = True
                    delta_ram = data.ram
                    delta_cpu = data.cpu
                else:  # default case: nothing happened or only processes were stopped or started
                    warning = True
                    delta_ram = data.ram - last_application_dict[name].ram
                    delta_cpu = data.cpu - last_application_dict[name].cpu
                process_change = data.process_change

                justification_data = JustificationData(
                    application=name,
                    started=started,
                    stopped=stopped,
                    process_change=process_change,
                    delta_ram=delta_ram,
                    delta_cpu=delta_cpu,
                    warning=warning
                )

                lj.justification_list.append(justification_data)
        last_application_dict = application_dict
