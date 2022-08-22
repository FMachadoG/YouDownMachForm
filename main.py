from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication
from pytube import YouTube
import re
from datetime import datetime, timedelta

def enablePathResol():
    if (form.checkBox_DownAudio.isChecked() == True or form.checkBox_DownVideo.isChecked() == True):
        form.pushButton_SelecFolder.setEnabled(True)

    else:
        form.lineEdit_Path.setToolTip('')
        form.lineEdit_Path.clear()

        form.pushButton_SelecFolder.setEnabled(False)
    
    if form.checkBox_DownVideo.isChecked() == True:
        form.radioButton_ResoHigh.setEnabled(True)
        form.radioButton_ResoLow.setEnabled(True)

    else:
        form.radioButton_ResoHigh.setEnabled(False)
        form.radioButton_ResoLow.setEnabled(False) 

def exitFormHome():
    msg = QMessageBox.question(form, "Exit", "Do you really want to go out?",  QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)

    if msg == QMessageBox.Ok:
        exit()

def selectPath():
    pathDir = QtWidgets.QFileDialog.getExistingDirectory()

    form.lineEdit_Path.setToolTip(pathDir)
    form.lineEdit_Path.setText(pathDir)

    return pathDir

def setInformation():
    url = form.lineEdit_URL.text()

    validationURL = validationUrl(url)

    if validationURL is True:
        yt = YouTube(url)

        downloadVideoAudio(yt)
        showInformation(yt)

    else:
        form.label_AllInformation.setText(validationURL)

def validationUrl(url):
    linkCode = url.replace("https://www.youtube.com", "").replace("https://youtu.be", "")
    validCodeURL = re.match(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", linkCode)

    if (url.__contains__('https://www.youtube.com') == False and url.__contains__('https://youtu.be') == False):
        return QMessageBox.about(form, "Warning", "Invalid URL! \nPlease, fill in a valid URL.")

    elif validCodeURL is None:
        return QMessageBox.about(form, "Warning", "Invalid CODE video! \nPlease, fill in a valid URL.")

    else:
        return True

def downloadVideoAudio(yt):
    if (form.checkBox_DownAudio.isChecked() == True or form.checkBox_DownVideo.isChecked() == True):

        pathDownload = form.lineEdit_Path.text()

        if pathDownload == "":
            selectPath()

        pathDownload = form.lineEdit_Path.text()

        if form.checkBox_DownVideo.isChecked() == True:

            if form.radioButton_ResoHigh.isChecked() == True:

                yVideo = yt.streams.get_highest_resolution()
                yVideoTitle = yVideo.title.replace(".", "_")

                yVideo.download(pathDownload, f'{yVideoTitle}-_Highest_YouDownMach.mp4')
                

            else:
                yVideo = yt.streams.get_lowest_resolution()
                yVideoTitle = yVideo.title.replace(".", "_")

                yVideo.download(pathDownload, f'{yVideoTitle}-Lowest_YouDownMach.mp4')
                

        if form.checkBox_DownAudio.isChecked() == True:

            yAudio = yt.streams.get_audio_only("mp4")
            yAudioTitle = yAudio.title.replace(".", "_")

            yAudio.download(pathDownload, f'{yAudioTitle}-YouDownMach.mp3')

def showInformation(yt):
    viewsAmountVideo = "{:,}".format(yt.views)
    viewsAmountVideo = viewsAmountVideo.replace(",", ".")

    publiDateVideo = yt.publish_date
    publiDateVideo = publiDateVideo.strftime("%b %d, %Y")

    timeVideo = yt.length
    timeVideo = "{:0>8}".format(str(timedelta(seconds=timeVideo)))

    dateNow = datetime.now()

    form.pushButton_CopyTitle.setEnabled(True)
    form.pushButton_CopyChannel.setEnabled(True)
    form.pushButton_CopyThumb.setEnabled(True)
        
    # Label OK
    form.label_AllInformation.setText(f"Done! {dateNow.strftime('%m/%d/%Y %H:%M:%S')}")

    # Title
    # form.label_TTitle.setText("Title")
    form.label_RTitle.setText(yt.title)

    # Views
    # form.label_TViews.setText("Views")
    form.label_RViews.setText(viewsAmountVideo)

    # Pubi date
    # form.label_TPubliDate.setText("Publishi date")
    form.label_RPubliDate.setText(publiDateVideo)

    # Author
    # form.label_TAuthor.setText("Author")
    form.label_RAuthor.setText(yt.author)

    # Time
    # form.label_TTime.setText("Time")
    form.label_RTime.setText(timeVideo)

    # Channel
    # form.label_TChannel.setText("Channel")
    form.label_RChannel.setText(yt.channel_url)

    # Thumb
    # form.label_TThumb.setText("Thumb")
    form.label_RThumb.setText(yt.thumbnail_url)

def copyTitle():
    print('Title')
    titleVideo = form.label_RTitle.text()
    QApplication.clipboard().setText(titleVideo)

def copyChannel():
    print('Channel')
    channelVideo = form.label_RChannel.text()
    QApplication.clipboard().setText(channelVideo)

def copyThumb():
    print('Thumb')
    thumbVideo = form.label_RThumb.text()
    QApplication.clipboard().setText(thumbVideo)

# def closeEvent(self, event):
#             close = QtWidgets.QMessageBox.question(self,
#                                          "QUIT",
#                                          "Are you sure want to stop process?",
#                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
#             if close == QtWidgets.QMessageBox.Yes:
#                 event.accept()
#             else:
#                 event.ignore()

app = QtWidgets.QApplication([])
form = uic.loadUi('formHome.ui')

versionYouDownMach = "0.1.0"
form.label_RVersion.setText(f"{versionYouDownMach}")

form.checkBox_DownAudio.clicked.connect(enablePathResol)
form.checkBox_DownVideo.clicked.connect(enablePathResol)
form.pushButton_Exit.clicked.connect(exitFormHome)
form.pushButton_SelecFolder.clicked.connect(selectPath)
form.pushButton_Ok.clicked.connect(setInformation)
form.pushButton_CopyTitle.clicked.connect(copyTitle)
form.pushButton_CopyChannel.clicked.connect(copyChannel)
form.pushButton_CopyThumb.clicked.connect(copyThumb)

form.show() 
app.exec()