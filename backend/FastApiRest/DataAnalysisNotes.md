# Features 

### Event Detection & Justification
Events occuring for RAM or CPU Usage can be detected for the entire pc or a single application
LogSense tries to "justify" these Events by looking at what happened in the last 5 minutes before a large delta occuring (such as applications closing/opening, processes closing/opening or a large time gap between measured). If a large delta occured without any reason it is flagged as a warning. CPU Event Detection works by using a Z-Test since normal Change Detection Algorithms worked poorly for it

#### Algorithms used: Pelting Change Detection for RAM, Statistical Z-Test for CPU
=> check if it works correctly

## Anomaly Detection 
LogSense is able to detect anomalies via a Z-test. In most cases, anomaly and events will overlap. Also Anomalies are not justified, but instead just highlighted. Theoretically, justification is possible albeit different as the anomaly values would be compared to the default values.
=> check if it works correctly
#### Algorithms used: Statistical Z-Test

## Custom Alerts (WIP)
Users are able to define Custom Alerts by uploading json files following a defined schema, this step should be simplified for an improved user experience however. 

Example:
[
    {
        "user_id": 1,
        "type": "Breaking threshold alert for chrome",
        "message": "Chrome has broken a defined threshold (90% RAM usage per pc or went over 5GB absolute usage)",
        "severity_level": 5,
        "conditions": [
            {
                "percentage_trigger_value": 0.9,
                "operator": ">=",
                "column": "ram",
                "application": "chrome"
            }
    }
]
Each time the user wants to see an overview of his applications or computers, an api call is fetched to retrieve and check for Custom Alerts. This means this happens on request as on ingest would be very ressource intensive and not useful unless push messages are available
=> implement
## Forecasting
LogSense is able to forecast/predict data points at future date points, currently by using a linear regression model. Currently it is only able to forecast available disk space, but it should be able to forecast a multitude of values.
=> make it more flexible, use other algorithms than linear regression
#### Algorithms used: Linear Regression

## Transformation, Validating and Grouping
LogSense groups together application data of a data point to calculate the total application usage at that time. Apart from that, it should check for any inconsistencies or faulty data points (TBD)
=> implement
## Corellations and Problem detection (TBD)
LogSense will be able to detect corellations between RAM and CPU Usage such as events occuring or events occuring at certain times of the day. This would help an user to find out when problems might occur next time.
=> implement
# Terms

### Running Data
Data which is always updated each minute the agent is running. Application-, Disk- and Network-Data fall under this umbrella term.

### Initial/State Data
Data which is only updated and set when the agent first connects with the backend or when the "state" of a pc changes i.e. ram is swapped out.