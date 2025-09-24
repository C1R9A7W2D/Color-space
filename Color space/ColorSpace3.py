import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class HSVConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("RGB to HSV Converter")
        self.root.geometry("1000x700")
        
        self.original_image = None
        self.hsv_image = None
        self.modified_hsv_image = None
        self.result_image = None
        
        self.hue_shift = 0
        self.saturation_scale = 1.0
        self.value_scale = 1.0
        
        self.setup_ui()
        
    def setup_ui(self):

        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        image_frame = ttk.Frame(self.root, padding="10")
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Button(control_frame, text="Загрузить изображение", 
                  command=self.load_image).pack(pady=5, fill=tk.X)
        
        ttk.Button(control_frame, text="Сохранить результат", 
                  command=self.save_image).pack(pady=5, fill=tk.X)
        
        ttk.Button(control_frame, text="Сбросить настройки", 
                  command=self.reset_settings).pack(pady=5, fill=tk.X)
    
        ttk.Label(control_frame, text="Сдвиг оттенка (H):").pack(pady=(20, 5))
        self.hue_scale = ttk.Scale(control_frame, from_=-180, to=180, 
                                  orient=tk.HORIZONTAL, command=self.update_hue)
        self.hue_scale.set(0)
        self.hue_scale.pack(fill=tk.X, pady=5)
        self.hue_label = ttk.Label(control_frame, text="0°")
        self.hue_label.pack()
        
        ttk.Label(control_frame, text="Насыщенность (S):").pack(pady=(20, 5))
        self.saturation_scale_widget = ttk.Scale(control_frame, from_=0, to=3, 
                                         orient=tk.HORIZONTAL, command=self.update_saturation)
        self.saturation_scale_widget.set(1.0)
        self.saturation_scale_widget.pack(fill=tk.X, pady=5)
        self.saturation_label = ttk.Label(control_frame, text="1.00")
        self.saturation_label.pack()
        
        ttk.Label(control_frame, text="Яркость (V):").pack(pady=(20, 5))
        self.value_scale_widget = ttk.Scale(control_frame, from_=0, to=3, 
                                    orient=tk.HORIZONTAL, command=self.update_value)
        self.value_scale_widget.set(1.0)
        self.value_scale_widget.pack(fill=tk.X, pady=5)
        self.value_label = ttk.Label(control_frame, text="1.00")
        self.value_label.pack()
        
        self.original_label = ttk.Label(image_frame, text="Оригинальное изображение")
        self.original_label.pack(pady=10)
        self.original_canvas = tk.Canvas(image_frame, width=400, height=300, bg='white')
        self.original_canvas.pack(pady=5)
        
        self.result_label = ttk.Label(image_frame, text="Результат (HSV → RGB)")
        self.result_label.pack(pady=10)
        self.result_canvas = tk.Canvas(image_frame, width=400, height=300, bg='white')
        self.result_canvas.pack(pady=5)
        
        self.info_label = ttk.Label(control_frame, text="Загрузите изображение для начала")
        self.info_label.pack(pady=20)
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        
        if file_path:
            try:
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    raise ValueError("Не удалось загрузить изображение")
                
                original_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)

                self.hsv_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)
                self.modified_hsv_image = self.hsv_image.copy()
                
                self.display_image(original_rgb, self.original_canvas)
                
                self.update_result()
                
                self.info_label.config(text=f"Изображение загружено: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при загрузке изображения: {str(e)}")
    
    def update_hue(self, value):
        self.hue_shift = int(float(value))
        self.hue_label.config(text=f"{self.hue_shift}°")
        self.update_result()
    
    def update_saturation(self, value):
        self.saturation_scale = float(value)
        self.saturation_label.config(text=f"{self.saturation_scale:.2f}")
        self.update_result()
    
    def update_value(self, value):
        self.value_scale = float(value)
        self.value_label.config(text=f"{self.value_scale:.2f}")
        self.update_result()
    
    def update_result(self):
        if self.hsv_image is not None:
            self.modified_hsv_image = self.hsv_image.copy().astype(np.float32)
            
            self.modified_hsv_image[:, :, 0] = (self.modified_hsv_image[:, :, 0] + self.hue_shift / 2) % 180
            
            self.modified_hsv_image[:, :, 1] = np.clip(
                self.modified_hsv_image[:, :, 1] * self.saturation_scale, 0, 255
            )
            
            self.modified_hsv_image[:, :, 2] = np.clip(
                self.modified_hsv_image[:, :, 2] * self.value_scale, 0, 255
            )
            
            modified_hsv_uint8 = self.modified_hsv_image.astype(np.uint8)
            
            result_bgr = cv2.cvtColor(modified_hsv_uint8, cv2.COLOR_HSV2BGR)
            
            result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)
            self.result_image = result_bgr 
            
            self.display_image(result_rgb, self.result_canvas)
    
    def display_image(self, image, canvas):
        h, w = image.shape[:2]
        scale_factor = min(400/w, 300/h)
        new_w, new_h = int(w * scale_factor), int(h * scale_factor)
        
        resized_image = cv2.resize(image, (new_w, new_h))
        
        bgr_image = cv2.cvtColor(resized_image, cv2.COLOR_RGB2BGR)
        
        photo = self.array_to_photo(bgr_image)
        
        canvas.delete("all")
        canvas.create_image(200, 150, image=photo, anchor=tk.CENTER)
        canvas.image = photo 
    
    def array_to_photo(self, image_array):
        """Конвертирует numpy array в tkinter PhotoImage"""
        rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        
        h, w = rgb_image.shape[:2]
        data = f'P6 {w} {h} 255 '.encode() + rgb_image.tobytes()
        return tk.PhotoImage(data=data, format='PPM')
    
    def save_image(self):
        if self.result_image is not None:
            file_path = filedialog.asksaveasfilename(
                title="Сохранить результат",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            
            if file_path:
                try:
                    cv2.imwrite(file_path, self.result_image)
                    messagebox.showinfo("Успех", f"Изображение сохранено как: {file_path}")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")
        else:
            messagebox.showwarning("Предупреждение", "Нет изображения для сохранения")
    
    def reset_settings(self):
        self.hue_scale.set(0)
        self.saturation_scale_widget.set(1.0)
        self.value_scale_widget.set(1.0)
        self.update_result()

def main():
    root = tk.Tk()
    app = HSVConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()