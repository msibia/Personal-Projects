import tkinter as tk
import paho.mqtt.client as mqttClient
import re
import pandas as pd
import matplotlib.pyplot as plt




########### Subscribe to MQTT and Publish to file  ####################
client = mqttClient.Client("Python") #Create new mqtt instance

def handle_option1_selection(event, *args):
    selected_option1 = option_var1.get()
    print(selected_option1)

def handle_option2_selection(event, *args):
    selected_option2 = option_var2.get()
    print(selected_option2)

def stop_execution():
    client.disconnect()
    client.loop_stop() #Stop listening
     
        
def run_code():
    selected_option1 = option_var1.get()
    selected_option2 = option_var2.get()

    def on_connect(client, userdata, flags, rc):

        if rc == 0:

            print("Connected to broker")

            global Connected  # Use global variable
            Connected = True  # Signal connection

        else:

            print("Connection failed")

    def on_message(client, userdata, message):
        
        file_path = fr'C:Users\Admin\Downloads\{selected_option1} {selected_option2}.txt' #define file path
        print("Message received: " + str(message.payload))
        with open(file_path,'a+') as f:
            f.write("Message received: " + str(message.payload) + "\n")
        print(file_path)

    Connected = False  # global variable for the state of the connection

    broker_address = "192.168.201.12"  # Broker address
    port = 1883  # Broker port
    user = "leocancercare"  # Connection username
    password = "LeOcC@Service"  # Connection password

    # set username and password
    client.username_pw_set(user, password=password)
    client.on_connect = on_connect  # attach function to callback
    client.on_message = on_message  # attach function to callback
    client.connect(broker_address, port, 60)  # connect
    client.subscribe(f"Emc/{selected_option2}/{selected_option1}")  # subscribe to topic
    
    client.loop_start()  # start listening
    
    
    

####################### GUI Component #################################################

# Create the main application window
root = tk.Tk()
root.title("mqttReader")
root.geometry("300x400")

#Create Dropdown Menu 1 to select Axis
label1 = tk.Label(root, text="Select Axis")
label1.place(x=10, y=10)
options1 = ["ACS_X", "ACS_Y", "MCS_Rotation","ACS_Z Left","ACS_Z Right", "ACS_2Dof Left", 
            "ACS_2Dof Right", "MCS_Pitch", "MCS_Roll", "CT_Tilt", "CT_Translation"] #CT axes need to be updated to actual axis names that will show up on the MQTT server. 
option_var1 = tk.StringVar(root)
option_var1.set(options1[0])  # Set default option
dropdown1 = tk.OptionMenu(root, option_var1, *options1)
dropdown1.place(x=10, y=30)
option_var1.trace_add("write", handle_option1_selection)

#Create Dropdown Menu 2 to select Topic
label2 = tk.Label(root, text="Select Topic")
label2.place(x=10, y=65)
options2 = ["Position", "Velocity", "State", "Sensor_Raw", "Sensor_Offset", "numberOfMovements", "operation Time"]
option_var2 = tk.StringVar(root)
option_var2.set(options2[0])  # Set default option
dropdown2 = tk.OptionMenu(root, option_var2, *options2)
dropdown2.place(x=10, y=85)
option_var2.trace_add("write", handle_option2_selection)




# Create buttom to run source code
run_button = tk.Button(root, text="Run", command=run_code)
run_button.place(x=10, y=130, width=78, height=30)

# Create a button to stop code
stop_button = tk.Button(root, text="Stop", command=stop_execution)
stop_button.place(x=10, y=170, width=78, height=30)

# Start the main event loop
root.mainloop()
