from Tkinter import *
from tkMessageBox import *
from win32api import GetSystemMetrics
import Acquisition_rest_position as rest_pos
import Acquisition_max_depth as max_depth
import os, time, subprocess, win32gui, win32con

global file_name_data, session, blockLength, trialLength, blockNumber

original_dir = os.getcwd()


def refresh_session():
    os.chdir(original_dir)
    ## Refresh folder ListBox
    folders = os.listdir("data/")
    num_folders = len(folders)
    Subject_List.delete(0, END)
    fold_count = 0
    if num_folders != 0:
        for fold in folders:
            fold_count = fold_count + 1
            Subject_List.insert(fold_count, fold)
    else:
        Subject_List.insert(1, "Empty")

    ## Refresh session ListBox
    if entry_user_id.get() != '':
        session_dir = "data/" + entry_user_id.get() + '/'
        sessions = os.listdir(session_dir)
        num_sessions = len(sessions)
        Session_List.delete(0, END)
        sessions_count = 0
        if num_sessions != 0:
            for sess in sessions:
                sess = os.path.splitext(sess)[0]  # gives only the basename of the filename.txt
                sessions_count = sessions_count + 1
                Session_List.insert(sessions_count, sess)
        else:
            Session_List.insert(1, "Empty")


def create_session():
    global session
    time_stamp = time.strftime('%m-%d-%y_%H-%M')
    user = entry_user_id.get()
    session = entry_session.get()
    refresh_session()
    # path_user = 'data/' + id + '/'
    data_path = "data/" + user + "/" + user + "_" + session + "_" + time_stamp + ".txt"
    if session != '' and user in os.listdir('data/'):
        f = open(data_path, 'w')
        f.close()
        print(data_path + ' created')
        if entry_user_id.get() != '':
            session_dir = "data/" + entry_user_id.get() + '/'
            sessions = os.listdir(session_dir)
            num_sessions = len(sessions)
            Session_List.delete(0, END)
            sessions_count = 0
            if num_sessions != 0:
                for sess in sessions:
                    sess = os.path.splitext(sess)[0]  # gives only the basename of the filename.txt
                    sessions_count = sessions_count + 1
                    Session_List.insert(sessions_count, sess)
            else:
                Session_List.insert(1, "Empty")
    else:
        print('Problem: Please check the session name or the user id')


def toggle():
    '''
    use
    t_btn.config('text')[-1]
    to get the present state of the toggle button
    '''
    if t_btn.config('text')[-1] == 'True':
        t_btn.config(text='False')
    else:
        t_btn.config(text='True')


def create_id_folder():
    os.chdir(original_dir)
    id = entry_user_id.get()
    if id in os.listdir('data/'):
        print("This subject is already registered")
    else:
        os.mkdir('data/' + id)
        print("The new subject %s has been  registered" % id)


def Aquisition_rest_position():
    message = rest_pos.aquisition_rest_position('workspace/rest_position.txt')
    print(message)


def Aquisition_depth_position():
    message2 = max_depth.acquisition_position('workspace/max_reaching_position.txt')
    print(message2)


def calibration():
    global process
    process_name = "calibration/Controller_Leap.py"
    arguments = []
    process = subprocess.Popen(["python", process_name])


def Center_Out_Reaching(blockLength, trialLength, blockNumber):
    global process
    refresh_parameters(blockLength, trialLength, blockNumber)
    process_name = "/Tasks/Center_out_Reaching/Controller_Leap.py"
    the_cwd = os.getcwd()
    process = subprocess.Popen("python " + the_cwd + process_name, shell=True)
    time.sleep(2)


def kill_subprocess():
    global process
    process.kill()
    os.system('TASKKILL /f /im H3DLoad.exe')


def refresh_parameters(blockLength, trialLength, blockNumber):
    EA_factor = str(EA_factor_scale.get())
    Target_factor = str(Target_factor_scale.get())
    Distance_to_target = str(Target_Zone_Size.get())
    ## Block_Length = str(Block_Length_entry.get()) #input in minutes
    ## Trial_Length = str(Trial_Length_entry.get()) #input in seconds
    ## Block_Number = str(Block_Number_entry.get())

    Block_Length = blockLength  # input in minutes
    Trial_Length = trialLength
    Block_Number = blockNumber
    hand_impaired_str = str(hand_impaired.get())
    friction_coeff = str(Sphere_friction_scale.get())
    modality_str = str(modality.get())

    # if askyesno('Verify', 'Really quit?'):
    #     showwarning('Yes', 'Not yet implemented')
    # else:
    #     showinfo('No', 'Quit has been cancelled')

    parameter_file = open('workspace/parameters.txt', 'w')
    parameter_file.write(
        "EA_factor,%s\nTarget_factor,%s\nDistance_to_target,%s\nBlock_Length,%s\nTrial_Length,%s\nhand_impaired_str,%s\nfriction_coeff,%s\nBlock_Number,%s\nModality,%s\n" % (
        EA_factor, Target_factor, Distance_to_target, Block_Length, Trial_Length, hand_impaired_str, friction_coeff,
        Block_Number, modality_str))
    parameter_file.close()
    print(EA_factor, "\n", Target_factor, "\n", Distance_to_target, "\n", Block_Length, "\n", Trial_Length, "\n",
          hand_impaired_str, "\n", friction_coeff, "\n", Block_Number)
    time_stamp = time.strftime('%m-%d-%y_%H-%M')
    # print "SELECTION"+str(Subject_List.curselection())
    if len(Subject_List.curselection()) != 0:
        user = str(Subject_List.get(Subject_List.curselection()))
        if len(Session_List.curselection()) != 0:
            session = str(Session_List.get(Session_List.curselection()))
            print(session)
            data_path = "data/" + user + "/" + session + ".txt"
            print(data_path)
            subject_file = open('workspace/subject.txt', 'w')
            subject_file.write(user)
            subject_file.close()
    else:
        if "default" not in os.listdir('data/'):
            os.mkdir("data/default")
        data_path = os.getcwd() + "/data/default/" + time_stamp + ".txt"
        subject_file = open('workspace/subject.txt', 'w')
        subject_file.write("Unknown")
        subject_file.close()
    datapath_filepath = 'resources/datapath_filepath.txt'
    file_path = open(datapath_filepath, 'w')
    file_path.write(data_path)
    file_path.close()


def Toggle_Advanced_Buttons():
    pass


def preEval():
    os.chdir(original_dir)
    id = entry_user_id.get()

    blockLength = 10
    trialLength = 10
    blockNumber = 1

    if id in os.listdir('data/'):
        print("This subject is already registered")
        create_session()
        calibration()
        Center_Out_Reaching(blockLength, trialLength, blockNumber)
    else:
        os.mkdir('data/' + id)
        print("The new subject %s has been  registered" % id)
        create_session()
        calibration()
        Center_Out_Reaching(blockLength, trialLength, blockNumber)


def postEval():
    os.chdir(original_dir)
    id = entry_user_id.get()

    blockLength = 10
    trialLength = 10
    blockNumber = 1

    if id in os.listdir('data/'):
        print("This subject is already registered")
        create_session()
        calibration()
        Center_Out_Reaching(blockLength, trialLength, blockNumber)
    else:
        os.mkdir('data/' + id)
        print("The new subject %s has been  registered" % id)
        create_session()
        calibration()
        Center_Out_Reaching(blockLength, trialLength, blockNumber)


def trial():
    os.chdir(original_dir)
    id = entry_user_id.get()

    blockLength = 6
    trialLength = 10
    blockNumber = 7

    if id in os.listdir('data/'):
        print("This subject is already registered")
        create_session()
        calibration()
        Center_Out_Reaching(blockLength, trialLength, blockNumber)
    else:
        os.mkdir('data/' + id)
        print("The new subject %s has been  registered" % id)
        create_session()
        calibration()
        Center_Out_Reaching(blockLength, trialLength, blockNumber)


def advanced_settingcmd():
    status_label.pack_forget()
    # status2_label.pack_forget()
    status3_label.pack_forget()
    status4_label.config(text="___________________________________________________________________")
    status5_label.config(text="___________________________________________________________________")
    # status6_label.pack_forget()
    # status7_label.pack_forget()

    parameter_frame.pack_forget()

    status2_label.config(
        text="These are the advanced settings. Please return to normal setting if you are not an expert", font=10)
    # status10_label.pack(side=TOP)

    # safe Settings

    '''safe_setting = Frame(root)
    safe_setting.pack( side=BOTTOM)'''

    advanced_setting_button.config(text="Safe Setting", command=safe_settingcmd)

    # safe_setting_button = Button(safe_setting, text="Safe Settings", fg= "blue", command=advanced_settingcmd)
    # safe_setting_button.grid(row= 0, column= 5,padx=2, pady=2)

    ## Advanced

    advanced.pack(side=BOTTOM)
    ##advanced = Frame(root,width=200,height=100)
    ##advanced.pack(side=BOTTOM, fill=X)

    ## Modality (GUEST IS FOR A SRLAB INDEPEDENT TRAINING OR RESERACH: in guest mode the user can choose directly with his
    ## arms the impaired side, while in the research mode the researcher choose it in the GUI
    modalities = ['GUEST', 'RESEARCH', 'Block Rand']
    modality = StringVar(root)
    modality.set('Block Rand')
    modality_label = Label(advanced, text="MODALITY", font=5)
    modality_choice = OptionMenu(advanced, modality, *modalities)
    modality_label.grid(row=0, column=1, rowspan=3, columnspan=3, padx=10, pady=10)
    modality_choice.grid(row=0, column=3, rowspan=3, columnspan=3, padx=10, pady=10)

    ## Error Augmentation

    EA_factor_scale = Scale(advanced, variable=EA_factor, label='Error Augmentation factor', orient=HORIZONTAL,
                            length=200,
                            tickinterval=0.5, resolution=0.1, from_=-1, to=2)
    EA_factor_scale.set(EA_factor)
    EA_factor_scale.grid(row=1, columnspan=2, padx=2, pady=4)

    ## Distance from home to target factor
    Target_factor_scale = Scale(advanced, variable=Target_factor, label='Target factor', orient=HORIZONTAL, length=250,
                                tickinterval=0.05, resolution=0.05, from_=0.05,
                                to=0.6)  # , activebackground = 'red', troughcolor = 'blue'
    # target_factor max must be .4 bc otherwise the leap might not detect
    Target_factor_scale.set(Target_factor)
    Target_factor_scale.grid(row=2, columnspan=2, padx=2, pady=4)

    ## Distance to hit the target
    Target_Zone_Size = Scale(advanced, variable=Distance_to_target, label='Zone of target', orient=HORIZONTAL,
                             length=200,
                             tickinterval=0.01, resolution=0.005, from_=0,
                             to=0.04)  # , activebackground = 'red', troughcolor = 'blue'

    Target_Zone_Size.set(Distance_to_target)
    Target_Zone_Size.grid(row=3, columnspan=2, padx=2, pady=4)

    ## Time of a session

    Block_Length_entry = Entry(advanced)
    Block_Length_entry.insert(END, Block_Length)
    Block_Length_label = Label(advanced, text="Rounds Length (minutes)")
    Block_Length_label.grid(row=4, column=1, padx=2, pady=4)
    Block_Length_entry.grid(row=4, column=0, padx=2, pady=4)

    ## Number of session

    Block_Number_entry = Entry(advanced)
    Block_Number_entry.insert(END, Block_Number)
    Block_Number_label = Label(advanced, text="Number of Rounds")
    Block_Number_label.grid(row=6, column=1, padx=2, pady=4)
    Block_Number_entry.grid(row=6, column=0, padx=2, pady=4)

    ## Time of the trial
    Trial_Length_entry = Entry(advanced)
    Trial_Length_entry.insert(END, Trial_Length)
    Trial_Length_label = Label(advanced, text="Trial Length (seconds)")
    Trial_Length_label.grid(row=4, column=2, padx=2, pady=4)
    Trial_Length_entry.grid(row=4, column=3, padx=2, pady=4)

    ## Side to treat
    hands_impaired = ['none', 'left', 'right']
    hand_impaired = StringVar(root)
    hand_impaired.set('None')

    ## Sphere Friction

    Sphere_friction_scale = Scale(advanced, variable=friction_coeff, label='Sphere Physic', orient=HORIZONTAL,
                                  length=200,
                                  tickinterval=5, resolution=5, from_=10,
                                  to=50)  # , activebackground = 'red', troughcolor = 'blue'

    Sphere_friction_scale.set(friction_coeff)
    Sphere_friction_scale.grid(row=3, column=2, columnspan=2, padx=2, pady=4)
    print(friction_coeff)

    hand_choice_label = Label(advanced, text="Paretic Limb: ", font=10)
    hand_choice = OptionMenu(advanced, hand_impaired, *hands_impaired)
    hand_choice_label.grid(row=1, column=1, rowspan=3, columnspan=10, padx=10, pady=10)
    hand_choice.grid(row=1, column=3, rowspan=3, columnspan=10, padx=10, pady=10)

    refresh_parameters_button = Button(advanced, text="Refresh parameters", font=12, command=refresh_parameters)
    refresh_parameters_button.grid(row=6, column=2, columnspan=2)

    status9_label = Label(advanced, text="\n", font=10)
    status9_label.grid(row=7, column=2, columnspan=2)


def safe_settingcmd():
    status_label.pack()
    status2_label.config(text="Let's start by filling the \"ID\" and \"Session\" fields, select the paretic limb,")
    status3_label.pack()
    status4_label.config(text="__________________________________________________________")
    status5_label.config(text="__________________________________________________________")
    # status6_label.pack()

    parameter_frame.pack()

    advanced.pack_forget()

    advanced_setting_button.config(text="Advanced Setting", command=advanced_settingcmd)


##############################################################################################################

root = Tk(className=" LookinGlass - Physiotherapist Interface")
# header

header = Frame(root, height="500")
header.pack(side=TOP, fill=X)

photo = PhotoImage(file="LookinGlass.png")
imgLabel = Label(header, image=photo)
imgLabel.pack(side=TOP)

status_label = Label(header, text="Welcome to LookinGlass.", font=10)
status2_label = Label(header, text="Let's start by filling the \"ID\" and \"Session\" fields, select the paretic limb,",
                      font=10)
status3_label = Label(header, text="then press \"PRE-EVALUATION\", \"TRIAL\", or \"POST-EVALUATION\" to start.",
                      font=10)
status4_label = Label(header, text="__________________________________________________________", font=10)
status5_label = Label(header, text="__________________________________________________________", font=10)
status6_label = Label(header, text="\n", font=10)

status5_label.pack(side=TOP)
status_label.pack(side=TOP)
status6_label.pack(side=BOTTOM)
status4_label.pack(side=BOTTOM)
status3_label.pack(side=BOTTOM)
status2_label.pack(side=BOTTOM)

## First part: User and folder settings


toolbar = Frame(root)
toolbar.pack(side=TOP)

user_id_label = Label(toolbar, text="ID: ", font=1)
session = Label(toolbar, text="Session: ", font=1)

user_id = StringVar()
entry_user_id = Entry(toolbar, text=user_id)
entry_session = Entry(toolbar)

user_id_label.grid(row=0)
session.grid(row=1)

entry_user_id.grid(row=0, column=1)
entry_session.grid(row=1, column=1)

hands_impaired = ['none', 'left', 'right']
hand_impaired = StringVar(root)
hand_impaired.set('None')

hand_choice_label = Label(toolbar, text="Paretic Limb: ", font=10)
hand_choice = OptionMenu(toolbar, hand_impaired, *hands_impaired)
hand_choice_label.grid(row=2, column=0, sticky=E)
hand_choice.grid(row=2, column=1, sticky=E)
# status7_label = Label(toolbar, text = "\n", font=10)
# status7_label.grid(row=3,column=1,sticky=E)


# Advanced Settings

advanced_setting = Frame(root)
advanced_setting.pack(side=BOTTOM)

status10_label = Label(advanced_setting, text="\n", font=10)
status10_label.pack(side=BOTTOM)

advanced_setting_button = Button(advanced_setting, text="Advanced Settings", fg="blue", command=advanced_settingcmd)
advanced_setting_button.pack(side=BOTTOM)

## Sessions definitions
toolbar2 = Frame(root)
toolbar2.pack(side=BOTTOM)

## toolbar2_title = Label(toolbar2, text="Action & Session",font=14)
## toolbar2_title.pack(padx=2, pady=2)

preEval_button = Button(toolbar2, text="PRE-EVALUATION", command=preEval)
preEval_button.grid(row=10, column=1, padx=2, pady=2)

trial_button = Button(toolbar2, text="TRIAL", command=trial)
trial_button.grid(row=10, column=5, padx=2, pady=2)

postEval_button = Button(toolbar2, text="POST-EVALUATION", command=postEval)
postEval_button.grid(row=10, column=7, padx=2, pady=2)

# status8_label = Label(toolbar2, text = "\n", font=10)
# status8_label.grid(row=,column=1,sticky=E)


# ******* Tuning of the parameters *******

global Block_Length, Trial_Length, Block_Number, EA_factor, Target_factor, Distance_to_target, friction_coeff
# default paramters
EA_factor = 1.3
Target_factor = 0.15
Distance_to_target = 0.02  # m
Block_Length = 6  # minutes
Block_Number = 7
Trial_Length = 10  # seconds (assuming a minimum of 100 trails at 2100 seconds/100 trails )
friction_coeff = 20
modality = 3

parameter_frame = Frame(root)
parameter_frame.pack(side=BOTTOM)

advanced = Frame(root)
advanced.pack(side=BOTTOM)

root.mainloop()