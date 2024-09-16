from tkinter import *
from tkinter import messagebox
from win32api import GetSystemMetrics
from fpdf import FPDF
from datetime import datetime
import Acquisition_rest_position as rest_pos
import Acquisition_max_depth as max_depth
import os, time, subprocess, win32gui, win32con

global file_name_data, session

original_dir = os.getcwd()


# forse da eliminare
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
        print(sessions)
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
    # refresh_session()
    # path_user = 'data/' + id + '/'
    #data_path = "data/" + user + "/" + user + "_" + session + "_" + time_stamp + ".txt"
    data_path = "data" + user + user + "_" + session + "_" + time_stamp + ".txt"
    if session != '' and user in os.listdir('data/'):
        f = open(data_path, 'w')
        f.close()
        print(data_path + ' created')
        if entry_user_id.get() != '':
            session_dir = "data/" + entry_user_id.get() + '/'
            sessions = os.listdir(session_dir)
            num_sessions = len(sessions)
            # Session_List.delete(0, END)
            sessions_count = 0
            if num_sessions != 0:
                for sess in sessions:
                    sess = os.path.splitext(sess)[0]  # gives only the basename of the filename.txt
                    sessions_count = sessions_count + 1
                    # Session_List.insert(sessions_count, sess)
            # else:
            # Session_List.insert(1, "Empty")
    else:
        print('Problem: Please check the session name or the user id')


# maybe to delete
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


def Center_Out_Reaching():
    global process
    refresh_parameters()
    process_name = "/Tasks/Center_out_Reaching/Controller_Leap.py"
    the_cwd = os.getcwd()
    process = subprocess.Popen("python " + the_cwd + process_name, shell=True)
    time.sleep(2)


def kill_subprocess():
    global process
    process.kill()
    os.system('TASKKILL /f /im H3DLoad.exe')


def refresh_parameters():
    if entry_user_id.get() != '':
        create_id_folder()
        create_session()

    EA_factor = str(EA_factor_scale.get())
    Target_factor = str(Target_factor_scale.get())
    Distance_to_target = str(Target_Zone_Size.get())
    Block_Length = str(Block_Length_entry.get())  # input in minutes
    Trial_Length = str(Trial_Length_entry.get())  # input in seconds
    Block_Number = str(Block_Number_entry.get())
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
    print("Subject_List" + str(Subject_List))
    print("SELECTION" + str(Subject_List.curselection()))
    # if len(Subject_List.curselection()) != 0:
    user = entry_user_id.get()
    session = entry_session.get()
    print(session)
    time_stamp = time.strftime('%m-%d-%y_%H-%M')
    data_path = "data/" + user + "/" + user + "_" + session + "_" + time_stamp + ".txt"
    print(data_path)
    subject_file = open('workspace/subject.txt', 'w')
    subject_file.write(user)
    subject_file.close()
    datapath_filepath = 'resources/datapath_filepath.txt'
    file_path = open(datapath_filepath, 'w')
    file_path.write(data_path)
    file_path.close()


def Toggle_Advanced_Buttons():
    pass


def save():
    time_stamp = time.strftime('%m-%d-%y_%H-%M')
    user = entry_user_id.get()
    session = entry_session.get()
    data_path = "data/" + user + "/" + user + "_" + session + "_" + time_stamp + ".pdf"

    f = open("TimeDate.txt", "w+")
    ff = open("patientInfo.txt", "w+")
    fff = open("patientScore.txt", "w+")
    ffff = open("treatmentInfo.txt", "w+")

    dateTimeObj = datetime.now()

    str_date = "Date: " + str(dateTimeObj.month) + '/' + str(dateTimeObj.day) + '/' + str(dateTimeObj.year) + "\n"
    str_time = "Time: " + str(dateTimeObj.hour) + ':' + str(dateTimeObj.minute) + "\n\n"

    str_userId = "User ID: " + user + "\n"
    str_session = "Treatment: " + session + "\n"
    str_imparedLimb = "Impared Limb: " + hand_impaired.get() + "\n\n"

    str_trainingBlockTime = "Training Block Time: " + Block_Length_entry.get() + " minutes" + "\n"
    str_numbTrainingBlocks = "Number of Training Blocks: " + Block_Number_entry.get() + "\n"
    str_movementCompletionTimeLimit = "Movement Completion Time Limit (Time to give up and go to the next movement): " + Trial_Length_entry.get() + " seconds" + "\n\n"

    f.write(str_date)
    f.write(str_time)

    ff.write(str_userId)
    ff.write(str_session)
    ff.write(str_imparedLimb)

    ffff.write(str_trainingBlockTime)
    ffff.write(str_numbTrainingBlocks)
    ffff.write(str_movementCompletionTimeLimit)

    #TO DO: improve this part!!
    fff.write(
        "Target Factor: .." + "\n" + "Percentage of the Reaching Range: .." + "\n" + "Accuracy of the Reaching: ..")

    f.close()
    ff.close()
    fff.close()
    ffff.close()

    title = 'Report'

    class PDF(FPDF):
        def up_header(self):
            # Position at 1.5 cm from bottom
            self.set_y(3)
            # Arial italic 8
            self.set_font('Helvetica', 'I', 8)
            # Text color in gray
            self.set_text_color(128)
            # Page number
            self.cell(0, 10, 'LookinGlass - Trayball', 0, 0, 'R')

        def header(self):
            # Arial bold 15
            self.set_font('Helvetica', 'B', 15)
            # Calculate width of title and position
            w = self.get_string_width(title) + 6
            self.set_x((210 - w) / 2)
            # Colors of frame, background and text
            self.set_draw_color(255, 255, 255)
            self.set_fill_color(255, 255, 255)
            self.set_text_color(220, 50, 50)
            # Thickness of frame (1 mm)
            self.set_line_width(1)
            # Title
            self.cell(w, 9, title, 1, 1, 'C', 1)
            # Line break
            self.ln(10)

        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Helvetica', 'I', 8)
            # Text color in gray
            self.set_text_color(128)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

        def chapter_title(self, label):
            # Arial 12
            self.set_font('Helvetica', 'U', 14)
            # Background color
            self.set_fill_color(255, 255, 255)
            # Title
            self.cell(0, 6, '%s' % (label), 0, 1, 'L', 1)
            # Line break
            self.ln(4)

        def chapter_body(self, name):
            # Read text file
            with open(name, 'rb') as fh:
                txt = fh.read().decode('latin-1')
            # Times 12
            self.set_font('Helvetica', '', 12)
            # Output justified text
            self.multi_cell(0, 5, txt)
            # Line break
            self.ln()

        def print_chapter(self, title, name):
            # self.add_page()
            self.chapter_title(title)
            self.chapter_body(name)

        def chapter_noTitle(self, name):
            self.chapter_body(name)

    pdf = PDF()
    pdf.add_page()
    pdf.set_title(title)
    pdf.set_author('Jules Verne')
    pdf.chapter_noTitle('TimeDate.txt')
    pdf.print_chapter('Patient Informations:', 'patientInfo.txt')
    pdf.print_chapter('Treatment Informations:', 'treatmentInfo.txt')
    pdf.print_chapter('Patient Score:', 'patientScore.txt')
    pdf.up_header()
    pdf.output(data_path, 'F')

    os.remove('C:/Users/Administrator/Documents/Trayball/Leap_Control_Federica/TimeDate.txt')
    os.remove('C:/Users/Administrator/Documents/Trayball/Leap_Control_Federica//patientInfo.txt')

    os.system('C:/Users/Administrator/Documents/Trayball/Leap_Control_Federica/' + data_path)


def advanced_settingcmd():
    # parameter_frame.pack_forget()
    advanced.place_forget()

    # preEval_button = Button(toolbar2, text="Calibration", command=Aquisition_rest_position)  # calibration)
    preEval_button.grid(row=10, column=1, padx=2, pady=2)

    advanced_setting_button.config(text="Home", command=lambda: [safe_settingcmd(), preEval_button.grid_forget()])
    advanced_setting_button.grid(row=10, column=3, padx=2, pady=2)

    advanced_setting_button2.config(text="Advanced Settings", command=advanced_settingcmd2)
    advanced_setting_button2.grid(row=10, column=4, padx=2, pady=2)

    toolbar.pack(side=TOP)

    user_id_label = Label(toolbar, text="ID")
    session = Label(toolbar, text="Treatment")

    # user_id = StringVar()
    # entry_user_id = Entry(toolbar, text=user_id)
    # entry_session = Entry(toolbar)

    user_id_label.grid(row=0, sticky=E)
    session.grid(row=1, sticky=E)

    entry_user_id.grid(row=0, column=1)
    entry_session.grid(row=1, column=1)

    ## Advanced

    advanced2.pack(side=TOP)

    '''global Block_Length, Trial_Length, Block_Number, EA_factor, Target_factor, Distance_to_target, friction_coeff
    # default paramters
    EA_factor = 1.3
    Target_factor = 0.15
    Distance_to_target = 0.02  # m
    Block_Length = 6  # minutes
    Block_Number = 7
    Trial_Length = 10  # seconds (assuming a minimum of 100 trails at 2100 seconds/100 trails )
    friction_coeff = 20
    modality = 1'''

    ## Modality (GUEST IS FOR A SRLAB INDEPEDENT TRAINING OR RESERACH: in guest mode the user can choose directly with his
    ## arms the impaired side, while in the research mode the researcher choose it in the GUI
    # modalities = ['GUEST', 'RESEARCH', 'Block Rand']
    # modality = StringVar(root)
    # modality.set('GUEST')
    # modality_label = Label(advanced2, text="MODALITY", font=5)
    # modality_choice = OptionMenu(advanced2, modality, *modalities)
    modality_label.grid(row=4, column=1, rowspan=3, columnspan=3, padx=10, pady=10)
    modality_choice.grid(row=4, column=3, rowspan=3, columnspan=3, padx=10, pady=10)

    ## Time of a session

    # Block_Length_entry = Entry(advanced2)
    # Block_Length_entry.insert(END, Block_Length)
    # Block_Length_label = Label(advanced2, text="Training Block Time (Minutes)")
    Block_Length_label.grid(row=1, column=2, padx=0, pady=4)
    Block_Length_entry.grid(row=1, column=3, padx=0, pady=4)

    ## Number of session

    # Block_Number_entry = Entry(advanced2)
    # Block_Number_entry.insert(END, Block_Number)
    # Block_Number_label = Label(advanced2, text="Number of Training Blocks")
    Block_Number_label.grid(row=2, column=2, padx=2, pady=4)
    Block_Number_entry.grid(row=2, column=3, padx=2, pady=4)

    ## Time of the trial
    # Trial_Length_entry = Entry(advanced2)
    # Trial_Length_entry.insert(END, Trial_Length)
    # Trial_Length_label = Label(advanced2,
    # text="Movement Completion Time Limit (Time to give up and go to the next movement - In Seconds)")
    Trial_Length_label.grid(row=3, column=2, padx=0, pady=4)
    Trial_Length_entry.grid(row=3, column=3, padx=0, pady=4)

    ## Side to treat
    # hands_impaired = ['none', 'left', 'right']
    # hand_impaired = StringVar(advanced2)
    # hand_impaired.set('None')

    # hand_choice_label = Label(advanced2, text="Paretic Limb: ", font=10)
    # hand_choice = OptionMenu(advanced2, hand_impaired, *hands_impaired)
    hand_choice_label.grid(row=7, column=1, rowspan=3, columnspan=10, padx=10, pady=10)
    hand_choice.grid(row=7, column=3, rowspan=3, columnspan=10, padx=10, pady=10)

    final_Buttons.pack(side=BOTTOM)

    refresh_parameters_button = Button(final_Buttons, text="APPLY", font=10, command=refresh_parameters)
    refresh_parameters_button.grid(row=10, column=5, columnspan=3)

    save_button = Button(final_Buttons, text="Generate a PDF Report (Not Work Right Now)", font=10, command=save)
    save_button.grid(row=10, column=1, columnspan=3)


def advanced_settingcmd2():
    # parameter_frame.pack_forget()
    # advanced2.pack_forget()

    # preEval_button = Button(toolbar2, text="Calibration", command=Aquisition_rest_position)  # calibration)
    preEval_button.grid(row=10, column=1, padx=2, pady=2)

    calibration_button.grid(row=10, column=0, padx=2, pady=2)
    rest_position.grid(row=10, column=8, padx=2, pady=2)

    advanced_setting_button.config(text="Home", command=lambda: [safe_settingcmd(), preEval_button.grid_forget(),
                                                                 calibration_button.grid_forget(),
                                                                 rest_position.grid_forget()])
    advanced_setting_button.grid(row=10, column=3, padx=2, pady=2)

    advanced_setting_button2.config(text="Settings",
                                    command=lambda: [advanced_settingcmd(), calibration_button.grid_forget(),
                                                     rest_position.grid_forget()])
    advanced_setting_button2.grid(row=10, column=4, padx=2, pady=2)

    toolbar.pack(side=TOP)
    user_id_label = Label(toolbar, text="ID")
    session = Label(toolbar, text="Treatment")

    # user_id = StringVar()
    # entry_user_id = Entry(toolbar, text=user_id)
    # entry_session = Entry(toolbar)

    user_id_label.grid(row=0, sticky=E)
    session.grid(row=1, sticky=E)

    entry_user_id.grid(row=0, column=1)
    entry_session.grid(row=1, column=1)

    ## Advanced

    # advanced.pack(side=RIGHT)
    advanced.place(x=10, y=130)

    ## Error Augmentation

    EA_factor_scale = Scale(advanced, variable=EA_factor, label='Error Augmentation factor', orient=HORIZONTAL,
                            length=340,
                            tickinterval=0.5, resolution=0.1, from_=-1, to=2)
    EA_factor_scale.set(EA_factor)
    EA_factor_scale.grid(row=1, column=1, padx=5, pady=4)

    ## Distance from home to target factor
    Target_factor_scale = Scale(advanced, variable=Target_factor, label='Distance to Targets', orient=HORIZONTAL,
                                length=340,
                                tickinterval=0.05, resolution=0.05, from_=0.05,
                                to=0.6)  # , activebackground = 'red', troughcolor = 'blue'
    # target_factor max must be .4 bc otherwise the leap might not detect
    Target_factor_scale.set(Target_factor)
    Target_factor_scale.grid(row=2, column=1, padx=2, pady=4)

    ## Distance to hit the target
    Target_Zone_Size = Scale(advanced, variable=Distance_to_target, label='Target Size', orient=HORIZONTAL, length=340,
                             tickinterval=0.01, resolution=0.005, from_=0,
                             to=0.04)  # , activebackground = 'red', troughcolor = 'blue'

    Target_Zone_Size.set(Distance_to_target)
    Target_Zone_Size.grid(row=3, column=1, padx=2, pady=4)

    ## Sphere Friction

    Sphere_friction_scale = Scale(advanced, variable=friction_coeff,
                                  label='Ball Friction (how difficult it is for the ball to fall off the plate)',
                                  orient=HORIZONTAL, length=340,
                                  tickinterval=5, resolution=5, from_=10,
                                  to=50)  # , activebackground = 'red', troughcolor = 'blue'

    Sphere_friction_scale.set(friction_coeff)
    Sphere_friction_scale.grid(row=4, column=1, padx=2, pady=4)
    print(friction_coeff)

    # advanced.pack(side=TOP)
    advanced2.place(x=380, y=190)

    # modality_label = Label(advanced2, text="MODALITY", font=5)
    # modality_choice = OptionMenu(advanced2, modality, *modalities)
    modality_label.grid(row=4, column=1, rowspan=3, columnspan=3, padx=10, pady=10)
    modality_choice.grid(row=4, column=3, rowspan=3, columnspan=3, padx=10, pady=10)

    ## Side to treat
    # hands_impaired = ['none', 'left', 'right']
    # hand_impaired = StringVar(advanced)
    # hand_impaired.set('None')

    # hand_choice_label = Label(advanced, text="Paretic Limb: ", font=10)
    # hand_choice = OptionMenu(advanced, hand_impaired, *hands_impaired)
    hand_choice_label.grid(row=7, column=1, rowspan=3, columnspan=10, padx=10, pady=10)
    hand_choice.grid(row=7, column=3, rowspan=3, columnspan=10, padx=10, pady=10)

    ## Time of a session

    # Block_Length_entry = Entry(advanced2)
    # Block_Length_entry.insert(END, Block_Length)
    # Block_Length_label = Label(advanced2, text="Training Block Time (Minutes)")
    Block_Length_label.grid(row=1, column=2, padx=0, pady=4)
    Block_Length_entry.grid(row=1, column=3, padx=0, pady=4)

    ## Number of session

    # Block_Number_entry = Entry(advanced2)
    # Block_Number_entry.insert(END, Block_Number)
    # Block_Number_label = Label(advanced2, text="Number of Training Blocks")
    Block_Number_label.grid(row=2, column=2, padx=2, pady=4)
    Block_Number_entry.grid(row=2, column=3, padx=2, pady=4)

    ## Time of the trial
    # Trial_Length_entry = Entry(advanced2)
    # Trial_Length_entry.insert(END, Trial_Length)
    # Trial_Length_label = Label(advanced2,
    # text="Movement Completion Time Limit (Time to give up and go to the next movement - In Seconds)")
    Trial_Length_label.grid(row=3, column=2, padx=0, pady=4)
    Trial_Length_entry.grid(row=3, column=3, padx=0, pady=4)

    '''global Block_Length, Trial_Length, Block_Number, EA_factor, Target_factor, Distance_to_target, friction_coeff
    # default paramters
    EA_factor = 1.3
    Target_factor = 0.15
    Distance_to_target = 0.02  # m
    Block_Length = 6  # minutes
    Block_Number = 7
    Trial_Length = 10  # seconds (assuming a minimum of 100 trails at 2100 seconds/100 trails )
    friction_coeff = 20
    modality = 1'''

    ## Modality (GUEST IS FOR A SRLAB INDEPEDENT TRAINING OR RESERACH: in guest mode the user can choose directly with his
    ## arms the impaired side, while in the research mode the researcher choose it in the GUI
    # modalities = ['GUEST', 'RESEARCH', 'Block Rand']
    # modality = StringVar(root)
    # modality.set('GUEST')
    '''modality_label = Label(advanced, text="MODALITY", font=5)
    modality_choice = OptionMenu(advanced, modality, *modalities)
    modality_label.grid(row=3, column=1, rowspan=3, columnspan=9, padx=10, pady=10)
    modality_choice.grid(row=3, column=2, rowspan=3, columnspan=9, padx=10, pady=10)

    ## Error Augmentation

    EA_factor_scale = Scale(advanced, variable=EA_factor, label='Error Augmentation factor', orient=HORIZONTAL,
                            length=340,
                            tickinterval=0.5, resolution=0.1, from_=-1, to=2)
    EA_factor_scale.set(EA_factor)
    EA_factor_scale.grid(row=1, column=1, padx=5, pady=4)

    ## Distance from home to target factor
    Target_factor_scale = Scale(advanced, variable=Target_factor, label='Distance to Targets', orient=HORIZONTAL,
                                length=340,
                                tickinterval=0.05, resolution=0.05, from_=0.05,
                                to=0.6)  # , activebackground = 'red', troughcolor = 'blue'
    # target_factor max must be .4 bc otherwise the leap might not detect
    Target_factor_scale.set(Target_factor)
    Target_factor_scale.grid(row=2, column=1, padx=2, pady=4)

    ## Distance to hit the target
    Target_Zone_Size = Scale(advanced, variable=Distance_to_target, label='Target Size', orient=HORIZONTAL, length=340,
                             tickinterval=0.01, resolution=0.005, from_=0,
                             to=0.04)  # , activebackground = 'red', troughcolor = 'blue'

    Target_Zone_Size.set(Distance_to_target)
    Target_Zone_Size.grid(row=3, column=1, padx=2, pady=4)

    ## Sphere Friction

    Sphere_friction_scale = Scale(advanced, variable=friction_coeff,
                                  label='Ball Friction (how difficult it is for the ball to fall off the plate)',
                                  orient=HORIZONTAL, length=340,
                                  tickinterval=5, resolution=5, from_=10,
                                  to=50)  # , activebackground = 'red', troughcolor = 'blue'

    Sphere_friction_scale.set(friction_coeff)
    Sphere_friction_scale.grid(row=4, column=1, padx=2, pady=4)
    print(friction_coeff)

    ## Time of a session

    #Block_Length_entry = Entry(advanced)
    #Block_Length_entry.insert(END, Block_Length)
    Block_Length_label = Label(advanced, text="Training Block Time (Minutes)")
    Block_Length_label.grid(row=1, column=2, padx=0, pady=4)
    Block_Length_entry.grid(row=1, column=3, padx=0, pady=4)

    ## Number of session

    #Block_Number_entry = Entry(advanced)
    #Block_Number_entry.insert(END, Block_Number)
    Block_Number_label = Label(advanced, text="Number of Training Blocks")
    Block_Number_label.grid(row=2, column=2, padx=2, pady=4)
    Block_Number_entry.grid(row=2, column=3, padx=2, pady=4)

    ## Time of the trial
    #Trial_Length_entry = Entry(advanced)
    #Trial_Length_entry.insert(END, Trial_Length)
    Trial_Length_label = Label(advanced,
                               text="Movement Completion Time Limit (Time to give up and go to the next movement - In Seconds)")
    Trial_Length_label.grid(row=3, column=2, padx=0, pady=4)
    Trial_Length_entry.grid(row=3, column=3, padx=0, pady=4)

    ## Side to treat
    #hands_impaired = ['none', 'left', 'right']
    #hand_impaired = StringVar(advanced)
    #hand_impaired.set('None')

    #hand_choice_label = Label(advanced, text="Paretic Limb: ", font=10)
    #hand_choice = OptionMenu(advanced, hand_impaired, *hands_impaired)
    hand_choice_label.grid(row=4, column=1, rowspan=3, columnspan=10, padx=10, pady=10)
    hand_choice.grid(row=4, column=2, rowspan=3, columnspan=10, padx=10, pady=10)'''

    final_Buttons.pack(side=BOTTOM)

    refresh_parameters_button = Button(final_Buttons, text="APPLY", font=10, command=refresh_parameters)
    refresh_parameters_button.grid(row=10, column=5, columnspan=3)

    save_button = Button(final_Buttons, text="Generate a PDF Report (Not Work Right Now)", font=10, command=save)
    save_button.grid(row=10, column=1, columnspan=3)


def safe_settingcmd():
    # parameter_frame.pack()

    advanced.place_forget()
    advanced2.place_forget()
    advanced2.pack_forget()
    toolbar.pack_forget()
    final_Buttons.pack_forget()

    advanced_setting_button.config(text="Settings", command=advanced_settingcmd)
    advanced_setting_button2.config(text="Advanced Settings", command=advanced_settingcmd2)


##############################################################################################################

root = Tk(className=" LookinGlass - Trayball")
root.geometry('1100x600')
# header

# header = Frame(root, height = "500")
# header.pack(side=TOP, fill=X)

# photo = PhotoImage(file="LookinGlass.png")
# imgLabel = Label(header, image=photo)
# imgLabel.pack(side=TOP)


## Buttons

toolbar2 = Frame(root)
toolbar2.pack(side=TOP)

trial_button = Button(toolbar2, text="Start", command=Center_Out_Reaching)
trial_button.grid(row=10, column=5, padx=2, pady=2)

postEval_button = Button(toolbar2, text="Stop", command=kill_subprocess)
postEval_button.grid(row=10, column=7, padx=2, pady=2)

# Advanced Settings

toolbar3 = Frame(root)
toolbar3.pack(side=TOP)

preEval_button = Button(toolbar3, text="Calibration", command=Aquisition_rest_position)  # calibration)
calibration_button = Button(toolbar3, text="Hardware Calibration", command=calibration)
rest_position = Button(toolbar3, text="Max Depth Measurement", command=Aquisition_depth_position)

advanced_setting = Frame(root)
advanced_setting.pack(side=TOP)

advanced_setting_button = Button(advanced_setting, text="Settings", fg="blue", command=advanced_settingcmd)
advanced_setting_button.grid(row=10, column=3, padx=2, pady=2)

advanced_setting_button2 = Button(advanced_setting, text=" Advanced Settings", fg="blue", command=advanced_settingcmd2)
advanced_setting_button2.grid(row=10, column=4, padx=2, pady=2)

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
modality = 1

Subject_List = Listbox(toolbar2, width=40, height=15, exportselection=0, selectmode=EXTENDED)
Session_List = Listbox(toolbar2, width=40, height=15, exportselection=0)

# parameter_frame = Frame(root)
# parameter_frame.pack( side=BOTTOM)

toolbar = Frame(root)
toolbar.pack(side=TOP)

user_id = StringVar()
entry_user_id = Entry(toolbar, text=user_id)
entry_session = Entry(toolbar)

advanced = Frame(root)
advanced.pack(side=BOTTOM)

'''hands_impaired = ['none', 'left', 'right']
hand_impaired = StringVar()
hand_impaired.set('None')

hand_choice_label = Label(advanced,text="Side affected ", font=10)
hand_choice = OptionMenu(advanced, hand_impaired, *hands_impaired)'''

# define the elements here otherwise the rest of the code won't see them
EA_factor_scale = Scale(advanced, variable=EA_factor, label='Error Augmentation factor', orient=HORIZONTAL, length=340,
                        tickinterval=0.5, resolution=0.1, from_=-1, to=2)
# EA_factor_scale.set(EA_factor)

Target_factor_scale = Scale(advanced, variable=Target_factor, label='Distance to Targets', orient=HORIZONTAL,
                            length=340,
                            tickinterval=0.05, resolution=0.05, from_=0.05,
                            to=0.6)  # , activebackground = 'red', troughcolor = 'blue'
# target_factor max must be .4 bc otherwise the leap might not detect
Target_factor_scale.set(Target_factor)

Target_Zone_Size = Scale(advanced, variable=Distance_to_target, label='Target Size', orient=HORIZONTAL, length=340,
                         tickinterval=0.01, resolution=0.005, from_=0,
                         to=0.04)  # , activebackground = 'red', troughcolor = 'blue'
Target_Zone_Size.set(Distance_to_target)

Sphere_friction_scale = Scale(advanced, variable=friction_coeff,
                              label='Ball Friction (how difficult it is for the ball to fall off the plate)',
                              orient=HORIZONTAL, length=340,
                              tickinterval=5, resolution=5, from_=10,
                              to=50)  # , activebackground = 'red', troughcolor = 'blue'
Sphere_friction_scale.set(friction_coeff)

'''Block_Length_entry = Entry(advanced)
Block_Length_entry.insert(END, Block_Length)
Block_Length_label = Label(advanced, text="Training Block Time (Minutes)")

Trial_Length_entry = Entry(advanced)
Trial_Length_entry.insert(END, Trial_Length)
Block_Number_label = Label(advanced, text="Number of Training Blocks")

Block_Number_entry = Entry(advanced)
Block_Number_entry.insert(END, Block_Number)
Trial_Length_label = Label(advanced,
                            text="Movement Completion Time Limit (Time to give up and go to the next movement - In Seconds)")
'''

advanced2 = Frame(root)
advanced2.pack(side=BOTTOM)

modalities = ['GUEST', 'RESEARCH', 'Block Rand']
modality = StringVar()
modality.set('GUEST')
modality_label = Label(advanced2, text="MODALITY", font=5)
modality_choice = OptionMenu(advanced2, modality, *modalities)

## Side to treat
# hands_impaired = ['none', 'left', 'right']
# hand_impaired = StringVar()
# hand_impaired.set('None')

hands_impaired = ['none', 'left', 'right']
hand_impaired = StringVar()
hand_impaired.set('None')

hand_choice_label = Label(advanced2, text="Paretic Limb: ", font=10)
hand_choice = OptionMenu(advanced2, hand_impaired, *hands_impaired)

Block_Length_entry = Entry(advanced2)
Block_Length_entry.insert(END, Block_Length)
Block_Length_label = Label(advanced2, text="Training Block Time (Minutes)")

Trial_Length_entry = Entry(advanced2)
Trial_Length_entry.insert(END, Trial_Length)
Block_Number_label = Label(advanced2, text="Number of Training Blocks")

Block_Number_entry = Entry(advanced2)
Block_Number_entry.insert(END, Block_Number)
Trial_Length_label = Label(advanced2,
                           text="Movement Completion Time Limit (Time to give up and go to the next movement - In Seconds)")

final_Buttons = Frame(root)
final_Buttons.pack(side=BOTTOM)

root.mainloop()