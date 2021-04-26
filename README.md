# SIMPT-SimulatingProcessTrees
We present a new tool that enables process owners to extract all the process aspects from their historical event data automatically, change these aspects, and re-run the process automatically using an interface. The combination of process mining and simulation techniques provides new evidence-driven ways to explore "what-if" questions. Therefore, assessing the effects of changes in process improvement is also possible. Our Python-based web-application provides a complete interactive platform to improve the flow of activities, i.e., process tree, along with possible changes in all the derived activity, resource, and process parameters. These parameters are derived directly from an event log without user-background knowledge.
## How to Run:
The tool is a Python-based web application based on the Django framework, to run the app:
- In the project directory
  - cmd: *python.exe manage.py runserver*
- Use *127.0.0.1:8000* in the browser

## How to Use:
In [this video](SIMPTIntroduction.mp4), we shortly explain the simulation process parameters and how to use the app (please download the video).

### Simulation Steps:

1.  ##### Upload an event log and click "Submit".

2.  ##### Map all the attributes of the event log and click "Submit".

3.  ##### Click "Statistics", you will see the process statistics of the input log.

4.  ##### Click "Process Tree", you will see the image of the generated process tree of the given log.

5.  ##### If you want to change the process tree, you can upload a new event log and click "Submit".

6.  ##### Click "Configuration" to configure the setting of our simulation.

7.  ##### Click "Submit" once you finished your setting.

8.  ##### If you want to change the duration, capacity, or limit, click "Further Configuration".

9.  ##### Click "Setting", you can check your currently used setting.

10.  ##### Click "Record" to record our upcoming simulation.

11.  ##### Click "Start" to start our simulation.

12.  ##### Click "Result", you will see the result of our simulation.

13.  ##### Click "Overview", you will see the overview of our simulation.

14.  ##### To change your setting, you can modify them by entering new entries and clicking "Submit" once again.

15.  ##### If you want to continue simulating based on the last simulation, click "Continue".

16.  ##### If you want to start a new simulation, click "Start" once again.

17.  ##### Click "Save" to save our simulation into simulationresult.csv and download it once the simulation is finished.



### Simulation Parameters in the Tool:
| Simulation Parameters in the Tool                                                                                                                             | Default Values                                                |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| Business Day: The trace and activity will only be simulated within our designated weekday.                                                                    | 1,2,3,4,5,6,7                                                 |
| Business Hour: The trace and activity will only be simulated within our designated hour.                                                                      | 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23 |
| Limit of Trace: The maximum number of traces can be simulated within the cycle time.                                                                          | float('inf')                                                  |
| Capacity of Trace: The maximum number of traces can be simulated simultaneously.                                                                              | float('inf')                                                  |
| Limit of Activity: The maximum number of activities can be simulated within the supply cycle.                                                                 |  float('inf')                                                             |
| Capacity of Activity: The maximum number of activities can be simulated simultaneously.                                                                       | float('inf')                                                  |
| Interrupt: The abnormal trace can't end normally by default. If we enter 'y', it will end normally in our simulation.                                         | 'n'                                                           |
| Miss: The abnormal trace can't start normally by default. If we enter 'y', it will start normally in our simulation.                                          | 'n'                                                           |
| Time Extension: The case will be simulated every hour by default. If we enter 'n', the case will only be simulated within the time range as in the given log. | 'y'                                                           |
| Duration of each Activity: The simulated time of each activity.                                                                                               | labeled on the suffix.                                        |
| Arrival Rate: The waiting time of two consecutive traces.                                                                                                     | The mean trace waiting time of our given log.                 |
| Supply Cycle: When the supply cycle is reached, all the counter of the limit will be cleared and re-counted, i.e. the resource will be supplied.              | float('inf')                                                  |
| Start Time: The start date of our simulation.                                                                                                                 | 2021-01-01 00:00:00                                           |
| Number of Generated Case: The number of the simulated trace.                                                                                                  | 100   


#### Process Tree:

*   ##### The syntax of the process tree we defined is based on PM4Py, so, please check the definition on PM4Py.

*   ##### To change the process tree, you can copy the original process tree, paste it to the text box, and modify based on it.

*   ##### Please be careful that there should be no space at the beginning and the end of your entry.

*   ##### Please make sure that the number of left and right parentheses is consistent.

*   ##### You should separate each operator, label, and closing parenthesis by space.

*   ##### Please make sure that the number of left and right parentheses is equal.

*   ##### For a more intuitive explanation, let's see the following example:

*   ###### Correct syntax: "+( 'spaghetti', ->( *( X( 'grill' ), τ ), 'pizza' ) )"

*   ###### Wrong syntax: " +( 'spaghetti', ->( *( X( 'grill' ), τ ), 'pizza' ) ) "

###### Explanation: There should be no space at the beginning and the end of the entry.

*   ###### Wrong syntax: "+( 'spaghetti', *( X( 'grill' ), τ ), 'pizza' ) )"

###### Explanation: The number of left and right parentheses is inconsistent.

*   ###### Wrong syntax: "+( 'spaghetti', ->(*( X( 'grill' ), τ), 'pizza' ))"

###### Explanation: Not all the components are separated by space.

*   ###### Wrong syntax: "&( 'spaghetti', ->( *( X( 'grill' ), τ ), 'pizza' ) )"

###### Explanation: Undefined operator '&'.

### Precautions:

*   ##### Only when the path of an event log is submitted can we click "Statistics".

*   ##### Only when the path of an event log is submitted can we click "Process Tree".

*   ##### Only when the setting of simulation is submitted and "Record" is clicked can we click "Setting".

*   ##### Only when the setting of simulation is submitted and "Record" is clicked can we click "Start".

*   ##### Only when "Start" is clicked can we click "Continue".

*   ##### Only when "Record" is clicked can we click "Save".

*   ##### Only when the configuration of simulation is submitted can we click "Further Configuration".

*   ##### Don't forget to click "Submit" once the entry is modified.

*   ##### Don't forget to click "Save" in the end.

*   ##### The blank entry at the input group will be considered as default.

### Contributors

- Shuai Jiao
- Mahsa Pourbafrani
### Citation
 - Pourbafrani, M., Jiao, Sh., van der Aalst, W.M.P.: SIMPT: Process improvement using interactive simulation of time-aware process trees. In: Proceedings of the DemonstrationTrack at RCIS 2021
