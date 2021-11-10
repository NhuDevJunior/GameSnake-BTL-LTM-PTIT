class ClientGUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ClientGUI, self).__init__(*args, **kwargs)
        self._singleplayer = False
        self._online = False
        self.init_ui()
    def init_ui(self):
        self.setFixedHeight(250)
        self.setFixedWidth(300)
        self.setWindowTitle("Snake")

        self.sm = QLabel("Singleplayer/Multiplayer",self)
        self.sm.move(20,10)
        self.sm.resize(150,30)
        
        self.sm_radio_group = QButtonGroup(self)
        self.single_player  = QRadioButton('Singleplayer', self)
        self.single_player.move(20,30)
        self.sm_radio_group.addButton(self.single_player)

        self.multi_player = QRadioButton('Multiplayer', self)
        self.multi_player.move(120,30)
        self.sm_radio_group.addButton(self.multi_player)
        
        
        # self.online_local = QLabel("Online/Local",self)
        # self.online_local.move(20,60)
        
        # self.ol_radio_group = QButtonGroup(self)

        # self.online = QRadioButton('Online', self)
        # self.online.move(20,80)
        # self.ol_radio_group.addButton(self.online)        

        # self.local = QRadioButton("Local",self)
        # self.local.move(120,80)
        # self.ol_radio_group.addButton(self.local)
        
        
        self.online_multiplayer = QLabel("Multiplayer:", self)
        self.online_multiplayer.resize(130, 20)
        self.online_multiplayer.move(20, 80)
        

        self.port_label = QLabel("Port:",self)
        self.port_label.move(20,100)
        self.port_input = QLineEdit(self)
        self.port_input.move(50, 105)
        self.port_input.resize(50,20)
        self.port_input.setText("65432")

        self.ip_label = QLabel("IP:", self)
        self.ip_label.move(120, 100)
        self.ip_input = QLineEdit(self)
        self.ip_input.move(150, 105)
        self.ip_input.resize(120,20)

        self.start_session = QPushButton("Start", self)
        self.start_session.move(215,200)
        self.start_session.resize(70,40)

        
        # self.local.clicked.connect(self.on_Local)
        # self.local.click()

        self.single_player.clicked.connect(self.on_Singleplayer)
        self.single_player.click()

        self.multi_player.clicked.connect(self.on_Multiplayer)

        # self.online.clicked.connect(self.on_online)


        self.start_session.clicked.connect(self.on_start)
    def on_start(self):
        if self._singleplayer:
            Snake()
        else:
            if self._online:
                Snake(True,str(self.ip_input.text()),int(self.port_input.text()))
            else:
                Snake(True)
    # def on_online(self):
    #     self.port_input.setEnabled(True)
    #     self.ip_input.setEnabled(True)
    #     self._online = True
    # def on_Local(self):
    #     self.port_input.setEnabled(False)
    #     self.ip_input.setEnabled(False)
    #     self._online = False
    def on_Singleplayer(self):
        # self.online.setEnabled(False)
        # self.local.setEnabled(False)
        self.port_input.setEnabled(False)
        self.ip_input.setEnabled(False)
        self._singleplayer = True
    def on_Multiplayer(self):
        # self.online.setEnabled(True)
        # self.local.setEnabled(True)
        self.port_input.setEnabled(True)
        self.ip_input.setEnabled(True)
        self._singleplayer = False