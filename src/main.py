from tkinter import Tk, Canvas, Button, PhotoImage, filedialog, Label, StringVar, Toplevel, ttk
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip
import cv2
import image_paths
import os
import time
import mediapipe as mp
import shutil


class VideoPlayerApp:
    def __init__(self):
        # 창 설정 및 생성
        self.window = Tk()
        self.window.title("Face Eraser")
        self.window.geometry("1280x720")
        self.window.configure(bg="#32333E")
        self.window.resizable(False, False)

        # 위젯 기본 생성
        self.create_widgets()

    # 첫 화면 기본 위젯들 배치 및 생성 함수
    def create_widgets(self):
        # 캔버스 생성
        self.canvas = Canvas(
            self.window,
            bg="#32333E",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        # 아이콘(얼굴탐지) 생성
        self.image_image_faceDetection = PhotoImage(file=image_paths.image_faceDetection)
        self.image_faceDetection = self.canvas.create_image(
            307.0,
            128.0,
            image=self.image_image_faceDetection
        )

        # 제목 생성
        self.image_image_title = PhotoImage(file=image_paths.image_title)
        self.image_title = self.canvas.create_image(
            640.0,
            135.0,
            image=self.image_image_title
        )

        # 아이콘(지우개) 생성
        self.image_image_earser = PhotoImage(file=image_paths.image_eraser)
        self.image_eraser = self.canvas.create_image(
            978.0,
            127.0,
            image=self.image_image_earser
        )

        # 버튼(설명 및 파일선택) 생성
        self.image_button_info_select = PhotoImage(file=image_paths.button_info_select)
        self.button_info_select = Button(
            self.window,
            image=self.image_button_info_select,
            borderwidth=0,
            highlightthickness=0,
            command=self.select_file,
            relief="flat"
        )
        self.button_info_select.place(
            x=380.0,
            y=223.0,
            width=521.0,
            height=330.0
        )

        # 버튼(파일선택) 생성
        self.image_button_select = PhotoImage(file=image_paths.button_select)
        self.button_select = Button(
            self.window,
            image=self.image_button_select,
            borderwidth=0,
            highlightthickness=0,
            command=self.select_file,
            relief="flat"
        )
        self.button_select.place(
            x=380.0,
            y=570.0,
            width=260.0,
            height=85.0
        )

        # 버튼(시작) 생성
        self.image_button_start = PhotoImage(file=image_paths.button_start)
        self.button_start = Button(
            self.window,
            image=self.image_button_start,
            borderwidth=0,
            highlightthickness=0,
            command=self.start_click,
            relief="flat"
        )
        self.button_start.place(
            x=640.0,
            y=570.0,
            width=260.0,
            height=85.0
        )

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("MP4 Files", "*.mp4")])
        if self.file_path:
            self.change_page1()

    def change_page1(self):
        self.button_info_select.destroy()

        self.image_image_preview = PhotoImage(file=image_paths.image_preview)
        self.image_preview = self.canvas.create_image(
            640.0,
            392.0,
            image=self.image_image_preview
        )

        self.label_thumbnail = Label(self.window, bg="#000000")
        self.label_thumbnail.place(
            x=410.0,
            y=253.0,
            width=360.0,
            height=270.0
        )

        # 업데이트 안해주면 아래 label_thumbnail의 width, height를 제대로 가져오지 못한다
        # update() 안 할거면 그냥 값 하드코딩하던가
        self.window.update()

        # 선택한 영상 불러오기, 프레임 정보
        self.cap = cv2.VideoCapture(self.file_path)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        # 썸네일 라벨 위젯 사이즈
        self.label_thumbnail_width = self.label_thumbnail.winfo_width()
        self.label_thumbnail_height = self.label_thumbnail.winfo_height()

        # 선택한 영상 사이즈
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 썸네일 라벨 위젯과 선택한 영상의 가로,세로 비율
        self.label_thumbnail_ratio = self.label_thumbnail_width / self.label_thumbnail_height
        self.video_ratio = self.video_width / self.video_height

        # 썸네일로 보여줄 이미지 크기를 비율에 맞춰 조정
        if self.label_thumbnail_ratio > self.video_ratio:
            self.thumbnail_width = int(self.label_thumbnail_height * self.video_ratio)
            self.thumbnail_height = self.label_thumbnail_height
        else:
            self.thumbnail_width = self.label_thumbnail_width
            self.thumbnail_height = int(self.label_thumbnail_width / self.video_ratio)

        # 영상의 첫 프레임 불러와 썸네일로 지정
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.thumbnail_width, self.thumbnail_height))
            image = Image.fromarray(frame)
            self.thumbnail_tk = ImageTk.PhotoImage(image)
            self.label_thumbnail.configure(image=self.thumbnail_tk)

        self.cap.release()

        # 파일 이름 가져오기
        file_name, file_ext = os.path.splitext(os.path.basename(self.file_path))
        filename = StringVar()
        filename.set(file_name)

        self.label_filename = Label(
            self.window,
            bg="#40424F",
            fg="#FFFFFF",
            font=("", 12),
            textvariable=filename,
            wraplength=100.0
        )
        self.label_filename.place(
            x=770.0,
            y=292.0,
            width=101.0,
            height=51.0
        )

        # 파일 길이 가져오기
        video = VideoFileClip(self.file_path)
        file_duration = video.duration
        video.close()
        fileduration = StringVar()
        fileduration.set(f"{file_duration} 초")

        self.label_fileduration = Label(
            self.window,
            bg="#40424F",
            fg="#FFFFFF",
            font=("", 12),
            textvariable=fileduration
        )
        self.label_fileduration.place(
            x=770.0,
            y=382.0,
            width=101.0,
            height=51.0
        )

        # 파일 크기 가져오기
        file_size = os.path.getsize(self.file_path)
        file_size_mb = file_size / (1024 * 1024)
        filesize = StringVar()
        filesize.set(f"{file_size_mb:.2f} MB")

        self.label_filesize = Label(
            self.window,
            bg="#40424F",
            fg="#FFFFFF",
            font=("", 12),
            textvariable=filesize
        )
        self.label_filesize.place(
            x=770.0,
            y=472.0,
            width=101.0,
            height=51.0
        )

    def start_click(self):
        if self.file_path:
            # self.directory_path = os.path.dirname(self.file_path)

            # # 디렉터리 경로와 파일 이름을 조합하여 파일 경로를 생성합니다.
            # self.temp_file_path = os.path.join(self.directory_path, "temp.mp4")
            
            self.temp_file_path="../temp/temp.mp4"
            self.change_page2()
            time.sleep(1)
            self.video_face_mosaic()

    def change_page2(self):
        self.canvas.delete(self.image_faceDetection)
        self.canvas.delete(self.image_title)
        self.canvas.delete(self.image_eraser)
        self.canvas.delete(self.image_preview)
        self.button_info_select.destroy()
        self.button_select.destroy()
        self.button_start.destroy()
        self.label_thumbnail.destroy()
        self.label_filename.destroy()
        self.label_fileduration.destroy()
        self.label_filesize.destroy()

        # 다 없애려 했는데 canvas같은건 남겨야됨 계속 쓰려면
        # widgets = self.window.winfo_children()
        # for widgets in widgets:
        #     widgets.destroy()

        self.image_image_frame = PhotoImage(file=image_paths.image_frame)
        self.image_frame = self.canvas.create_image(
            640.0,
            320.0,
            image=self.image_image_frame
        )

        self.label_frame = Label(self.window, bg="#000000")
        self.label_frame.place(
            x=320.0,
            y=76.0,
            width=640.0,
            height=480.0
        )

        self.window.update()

        self.label_frame_width = self.label_frame.winfo_width()
        self.label_frame_height = self.label_frame.winfo_height()

        self.label_frame_ratio = self.label_frame_width / self.label_frame_height

        if self.label_frame_ratio > self.video_ratio:
            self.frame_width = int(self.label_frame_height * self.video_ratio)
            self.frame_height = self.label_frame_height
        else:
            self.frame_width = self.label_frame_width
            self.frame_height = int(self.label_frame_width / self.video_ratio)

        self.image_button_stop = PhotoImage(file=image_paths.button_stop)
        self.button_stop = Button(
            self.window,
            image=self.image_button_stop,
            borderwidth=0,
            highlightthickness=0,
            command=self.stop_click,
            relief="flat"
        )
        self.button_stop.place(
            x=1135.0,
            y=55.0,
            width=90.0,
            height=90.0
        )

        self.progress_bar = ttk.Progressbar(
            self.window,
            mode='determinate',
            maximum=self.total_frames
        )
        self.progress_bar.place(
            x=240,
            y=600,
            width=720.0,
            height=40.0
        )

        self.percent = StringVar()
        self.percent.set("0%")
        self.label_progress = Label(
            self.window,
            font=("", 12),
            textvariable=self.percent
        )
        self.label_progress.place(
            x=960.0,
            y=600.0,
            width=80.0,
            height=40.0
        )

    def stop_click(self):
        self.is_processing = False

    def video_face_mosaic(self):
        cap = cv2.VideoCapture(self.file_path)
        fps = self.fps
        video_width = self.video_width
        video_height = self.video_height
        frame_width = self.frame_width
        frame_height = self.frame_height

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        output_path = self.temp_file_path
        out = cv2.VideoWriter(output_path, fourcc, fps, (video_width, video_height))

        self.processed_frames = 0
        self.is_processing = True

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            if ret:
                frame = self.detect_and_mosaic_faces(frame)
                out.write(frame)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (frame_width, frame_height))
                image = Image.fromarray(frame)
                self.image_tk = ImageTk.PhotoImage(image)
                self.label_frame.configure(image=self.image_tk)

                self.processed_frames += 1
                self.progress_bar['value'] = self.processed_frames

                per = int(self.processed_frames / self.total_frames * 100)
                self.percent.set("{}%".format(per))

                self.window.update()

            if cv2.waitKey(1) & 0xFF == ord('q') or not self.is_processing:
                break

        cap.release()
        out.release()

        if self.is_processing:
            self.show_message_complete()
        else:
            self.show_message_stop()

    def detect_and_mosaic_faces(self, image):
        minDetectionCon = 0.3
        mp_face_detection = mp.solutions.face_detection
        face_detection = mp_face_detection.FaceDetection(minDetectionCon)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = face_detection.process(image_rgb)

        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                h, w, c = image.shape
                x, y, w, h = int(bbox.xmin * w), int(bbox.ymin * h), \
                    int(bbox.width * w), int(bbox.height * h)
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0
                if w < 0:
                    w = 0
                if h < 0:
                    h = 0
                image = self.apply_mosaic(image, (x, y, w, h))

        return image

    def apply_mosaic(self, image, face_location, scale=0.05):
        x, y, w, h = face_location
        roi = image[y:y + h, x:x + w]
        roi = cv2.blur(roi, (50, 50))
        image[y:y + h, x:x + w] = roi

        return image

    def show_message_complete(self):
        self.message_window = Toplevel(self.window)
        self.message_window.title("완료")
        self.message_window.geometry(
            "+{}+{}".format(
                self.window.winfo_x() + self.window.winfo_width() // 2 - self.message_window.winfo_width() // 2,
                self.window.winfo_y() + self.window.winfo_height() // 2 - self.message_window.winfo_height() // 2))

        message_label = Label(self.message_window, text="모자이크 처리가 완료되었습니다!")
        message_label.pack(padx=20, pady=20)

        close_button = Button(self.message_window, text="확인", command=self.close_message)
        close_button.pack(pady=10)

        self.message_window.transient(self.window)
        self.message_window.grab_set()
        self.window.wait_window(self.message_window)

    def close_message(self):
        self.message_window.destroy()
        self.change_page3()

    def show_message_stop(self):
        self.message_window = Toplevel(self.window)
        self.message_window.title("중지")
        self.message_window.geometry(
            "+{}+{}".format(
                self.window.winfo_x() + self.window.winfo_width() // 2 - self.message_window.winfo_width() // 2,
                self.window.winfo_y() + self.window.winfo_height() // 2 - self.message_window.winfo_height() // 2))

        message_label = Label(self.message_window, text="모자이크 처리가 중지되었습니다!\n홈 화면으로 돌아갑니다.")
        message_label.pack(padx=20, pady=20)

        close_button = Button(self.message_window, text="확인", command=self.return_home)
        close_button.pack(pady=10)

        self.message_window.transient(self.window)
        self.message_window.grab_set()
        self.window.wait_window(self.message_window)

    def return_home(self):
        self.message_window.destroy()

        widgets = self.window.winfo_children()
        for widget in widgets:
            widget.destroy()
        self.create_widgets()

    def change_page3(self):
        self.button_stop.destroy()
        self.progress_bar.destroy()
        self.label_progress.destroy()
        self.label_frame.configure(image=None)
        self.image_tk.__del__()

        self.image_button_home = PhotoImage(file=image_paths.button_home)
        self.button_home = Button(
            self.window,
            image=self.image_button_home,
            borderwidth=0,
            highlightthickness=0,
            command=self.home_click,
            relief="flat"
        )
        self.button_home.place(
            x=1135.0,
            y=55.0,
            width=90.0,
            height=90.0
        )

        self.video_path = self.temp_file_path

        self.temp_cap = cv2.VideoCapture(self.video_path)
        self.frame_index = 0
        self.temp_fps = self.temp_cap.get(cv2.CAP_PROP_FPS)
        self.is_playing = False

        self.play_button = Button(
            self.window,
            text="Play",
            command=self.toggle_play
        )
        self.play_button.place(
            x=620.0,
            y=556.0,
            width=40.0,
            height=20.0
        )

        self.image_button_save = PhotoImage(file=image_paths.button_save)
        self.button_save = Button(
            self.window,
            image=self.image_button_save,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_file,
            relief="flat"
        )
        self.button_save.place(
            x=510.0,
            y=597.5,
            width=260.0,
            height=85.0
        )

    def update_video(self):
        if self.is_playing:
            ret, frame = self.temp_cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.frame_width, self.frame_height))
                image = Image.fromarray(frame)
                self.video_tk = ImageTk.PhotoImage(image)
                self.label_frame.configure(image=self.video_tk)
                self.frame_index += 1
            else:
                self.is_playing = False  # 영상 재생이 끝나면 재생 상태를 False로 설정
                self.play_button.configure(text="Play")
                self.temp_cap.release()
                self.temp_cap = cv2.VideoCapture(self.video_path)  # 영상을 처음부터 다시 재생하기 위해 재생 파일을 다시 열기
                self.frame_index = 0
                return  # 영상 재생이 끝났으므로 함수 종료
            self.window.after(int(1000 / self.temp_fps), self.update_video)

    def toggle_play(self):
        if not self.is_playing:
            self.is_playing = True
            self.play_button.configure(text="Pause")
            self.update_video()
        else:
            self.is_playing = False
            self.play_button.configure(text="Play")

    def save_file(self):
        self.save_path = filedialog.asksaveasfilename(
            title="파일 저장",
            defaultextension=".mp4",
            filetypes=[("MP4 파일", "*.mp4")]
        )

        if self.save_path:
            self.temp_cap.release()
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
            self.destination = os.path.normpath(os.path.join(self.script_dir, self.video_path))

            shutil.copy(self.destination, self.save_path)

            self.temp_cap = cv2.VideoCapture(self.video_path)
            self.temp_cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)

            self.show_message_save()

    def show_message_save(self):
        self.message_window = Toplevel(self.window)
        self.message_window.title("완료")
        self.message_window.geometry(
            "+{}+{}".format(
                self.window.winfo_x() + self.window.winfo_width() // 2 - self.message_window.winfo_width() // 2,
                self.window.winfo_y() + self.window.winfo_height() // 2 - self.message_window.winfo_height() // 2))

        message_label = Label(self.message_window, text="영상 저장이 완료되었습니다!")
        message_label.pack(padx=20, pady=20)

        close_button = Button(self.message_window, text="확인", command=lambda: self.message_window.destroy())
        close_button.pack(pady=10)

        self.message_window.transient(self.window)
        self.message_window.grab_set()
        self.window.wait_window(self.message_window)

    def home_click(self):
        widgets = self.window.winfo_children()
        for widget in widgets:
            widget.destroy()
        self.create_widgets()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = VideoPlayerApp()
    app.run()
