
# Di chuyển con trỏ chuột đến vị trí cụ thể:
# x, y: Tọa độ của vị trí cần di chuyển đến.
# duration: Thời gian (tính bằng giây) để di chuyển con trỏ đến vị trí (tùy chọn).
# pyautogui.moveTo(x, y, duration)


# Di chuyển tương đối từ vị trí hiện tại:
# pyautogui.moveRel(100, 100, 1)


# Nhấp chuột (trái, phải, giữa):
# pyautogui.click(x, y, button='left')
# pyautogui.rightClick(x, y)
# pyautogui.middleClick(x, y)


# Nhấp đúp chuột:
# pyautogui.doubleClick(x, y)

# Kéo và thả:
# pyautogui.dragTo(x, y, duration)
# pyautogui.dragRel(xOffset, yOffset, duration)


# Lấy kích thước màn hình:
# screenWidth, screenHeight = pyautogui.size()
# print(screenHeight) 
# 1080
# print(screenWidth)
# 1920

# Lấy vị trí hiện tại của con trỏ chuột:
# currentMouseX, currentMouseY = pyautogui.position()
# print(currentMouseX)
# print(currentMouseY)


#Chụp ảnh màn hình và lưu thành file:
# screenshot = pyautogui.screenshot('screenshot.png')


#Cuộn lên hoặc xuống:
# pyautogui.scroll(500)  # Cuộn lên 500 đơn vị
# pyautogui.scroll(-500)  # Cuộn xuống 500 đơn vị


import cv2
import pyautogui
import mediapipe
import math

class HandGestureControl:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.capture_hands = mediapipe.solutions.hands.Hands()
        self.drawing_option = mediapipe.solutions.drawing_utils
        self.screenWidth, self.screenHeight = pyautogui.size()
        self.with_frame = 0
        self.height_frame = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.prev_y = None

    def draw_thumb_and_index(self, thumb_tip, index_tip):
        """Vẽ các điểm landmark của ngón cái và ngón trỏ, đồng thời điều khiển con trỏ chuột"""
        self.x1 = int(thumb_tip.x * self.with_frame)
        self.y1 = int(thumb_tip.y * self.height_frame)
        cv2.circle(self.image, (self.x1, self.y1), 15, (0, 255, 0), 2)

        self.x2 = int(index_tip.x * self.with_frame)
        self.y2 = int(index_tip.y * self.height_frame)
        x_inScreen = int(self.x2 * self.screenWidth / self.with_frame)
        y_inScreen = int(self.y2 * self.screenHeight / self.height_frame)
        cv2.circle(self.image, (self.x2, self.y2), 15, (0, 255, 0), 2)
        pyautogui.moveTo(x_inScreen, y_inScreen, 0)

    def click_if_close(self):
        """Nhấp chuột nếu khoảng cách giữa ngón cái và ngón trỏ đủ gần"""
        dis = math.sqrt((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2)
        if dis < 40:
            x_inScreen = int(self.x2 * self.screenWidth / self.with_frame)
            y_inScreen = int(self.y2 * self.screenHeight / self.height_frame)
            pyautogui.click(x_inScreen, y_inScreen, button='left')

    def is_two_fingers_pinch_alt_tab(self ,IndexTip, Middle_Tip):
        dis = math.sqrt((IndexTip.x - Middle_Tip.x) ** 2 + (IndexTip.y - Middle_Tip.y) ** 2)
        if  dis < 0.05:
            pyautogui.hotkey('ctrl', 'tab')
    def is_two_fingers_pinch_alt_tab(self ,IndexTip, Middle_Tip):
        dis = math.sqrt((IndexTip.x - Middle_Tip.x) ** 2 + (IndexTip.y - Middle_Tip.y) ** 2)
        if  dis < 0.05:
            pyautogui.hotkey('ctrl', 'tab')

    def is_two_fingers_pinch_scroll_down(self ,Thumb_tip, Pinky_Tip):
        dis = math.sqrt((Thumb_tip.x - Pinky_Tip.x) ** 2 + (Pinky_Tip.y - Thumb_tip.y) ** 2)
        if dis < 0.15:
            pyautogui.scroll(-100)

    def is_two_fingers_pinch_scroll_up(self ,Thumb_tip, Pinky_Tip):
        dis = math.sqrt((Thumb_tip.x - Pinky_Tip.x) ** 2 + (Pinky_Tip.y - Thumb_tip.y) ** 2)
        if dis < 0.15 :
            pyautogui.scroll(100)

    def run(self):
        """Chạy vòng lặp chính để xử lý hình ảnh và nhận diện cử chỉ"""
        while True:
            _, self.image = self.camera.read()
            self.image = cv2.flip(self.image, 1)
            self.height_frame, self.with_frame, _ = self.image.shape
            rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

            output_hands = self.capture_hands.process(rgb_image)
            hands = output_hands.multi_hand_landmarks

            if hands:
                for hand in hands:
                    self.drawing_option.draw_landmarks(self.image, hand, mediapipe.solutions.hands_connections.HAND_CONNECTIONS)
                    allLandMark = hand.landmark

                    # Vẽ điểm ngón cái và ngón trỏ, điều khiển chuột theo ngón trỏ
                    self.draw_thumb_and_index(allLandMark[4], allLandMark[8])
                    # Kiểm tra cử chỉ nhấp chuột ngón cái và ngón trỏ
                    self.click_if_close()
                    # Kiểm tra Alt + Tab ngón trỏ và ngón giữa
                    self.is_two_fingers_pinch_alt_tab(allLandMark[8], allLandMark[12])
                    # Kiểm tra cuộn xuống ngón cái và ngón út
                    self.is_two_fingers_pinch_scroll_down(allLandMark[4], allLandMark[20])
                    # Kiểm tra cuộn lên ngón cái và ngón áp út
                    self.is_two_fingers_pinch_scroll_up(allLandMark[4], allLandMark[16])

            cv2.imshow("Hand movement video capture", self.image)

            if cv2.waitKey(1) == ord("q"):
                break

        self.camera.release()
        cv2.destroyAllWindows()


# Tạo đối tượng và chạy chương trình
if __name__ == "__main__":
    control = HandGestureControl()
    control.run()
