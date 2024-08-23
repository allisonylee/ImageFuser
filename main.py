import os.path
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image
import imutils
import pywt
import numpy as np
import customtkinter
import cv2

class GUI:

    def __init__(self):

        self.root = customtkinter.CTk()
        customtkinter.set_appearance_mode('light')
        customtkinter.set_default_color_theme('dark-blue')
        self.root.geometry('1000x1000')
        self.root.title('ImageFuser')

        self.gen_description = tk.Label(self.root,
                                           text='All images should be grayscale. Images will be saved as .tif files.',
                                           font=('Times New Roman', 18))
        self.gen_description.pack(pady=10)

        self.fuse_button = customtkinter.CTkButton(self.root, text='Fuse images', font=('Times New Roman', 14), command=self.fuse_images)
        self.fuse_button.pack(pady=20)

        self.fuse_description = tk.Label(self.root, text='Fusing: You will be prompted for (1) images to upload, and (2) a location to save fused image to.\n\nImages must all be of the same dimensions and have no manually added scale. Images will automatically be aligned before fusion. Fusion of many images will take longer.', font=('Times New Roman', 12))
        self.fuse_description.pack()

        self.resize_button = customtkinter.CTkButton(self.root, text='Resize images', font=('Times New Roman', 14), command=self.resize_images)
        self.resize_button.pack(pady=20)

        self.resize_description = tk.Label(self.root, text='Resizing: You will be prompted for (1) a height and width to resize images to, (2) images to upload, and (3) a location to save resized images to.', font=('Times New Roman', 12))
        self.resize_description.pack()

        self.crop_button = customtkinter.CTkButton(self.root, text='Crop images', font=('Times New Roman', 14), command=self.crop_images)
        self.crop_button.pack(pady=20)

        self.crop_description = tk.Label(self.root, text='Cropping: You will be prompted for (1) dimensions to crop to, (2) images to upload, and (3) a location to save cropped images to.', font=('Times New Roman', 12))
        self.crop_description.pack()

        self.get_frames_button = customtkinter.CTkButton(self.root, text='Extract frames from video', font=('Times New Roman', 14), command=self.get_frames)
        self.get_frames_button.pack(pady=20)

        self.get_frames_description = tk.Label(self.root, text='Frame extraction: You will be prompted for (1) a video to upload, and (2) a location to save frames to.', font=('Times New Roman', 12))
        self.get_frames_description.pack()

        self.root.mainloop()

    def resize_images(self):
        try:
            #ask height + width
            height = tk.simpledialog.askinteger(title='Height', prompt='Enter desired height (pixels):')
            width = tk.simpledialog.askinteger(title='Width', prompt='Enter desired width (pixels):')

            if height < 1 or width < 1:
                tk.messagebox.showerror(title='Invalid input', message='Height and width must be positive integers')
                return

            #select files
            paths = filedialog.askopenfilenames(title='Choose images',
                                                filetypes=[('JPEG files', '.jpeg .jpg'), ('TIFF/TIF files', '.tiff .tif'),
                                                        ('PNG files', '.png')])

            if paths:
                self.upload_message = tk.Label(self.root, text=f'Files uploaded successfully', font=('Times New Roman', 14))
                self.upload_message.pack()
                self.upload_message.after(10000, self.upload_message.destroy)
            else:
                tk.messagebox.showerror(title='Invalid input', message='No files chosen')
                self.upload_error_message = tk.Label(self.root, text=f'Files not uploaded successfully', font=('Times New Roman', 14))
                self.upload_error_message.pack()
                self.upload_error_message.after(10000, self.upload_error_message.destroy)
                return

            #resize
            image_files = []
            counter = 0
            for path in paths:
                image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                try:
                    resized_file = imutils.resize(image, width=width, height=height)
                except Exception as e:
                    tk.messagebox.showerror(title='Error', message=e)
                    self.saved_error_message = tk.Label(self.root, text=f'Files not resized successfully',
                                                        font=('Times New Roman', 14))
                    self.saved_error_message.pack()
                    self.saved_error_message.after(10000, self.saved_error_message.destroy)
                    return
                image_files.append(resized_file)
                counter += 1

            #choose directory
            if image_files:
                directory = filedialog.askdirectory(title='Choose directory')
            else:
                directory = []
            if directory:
                i = 0
                for image in image_files:
                    #save file
                    path = os.path.join(directory, f'resized_image{i}.tif')
                    cv2.imwrite(path, image)
                    i += 1
                    self.saved_message = tk.Label(self.root, text=f'File saved successfully as {path}', font=('Times New Roman', 14))
                    self.saved_message.pack()
                    self.saved_message.after(5000, self.saved_message.destroy)
                self.saved_message2 = tk.Label(self.root, text=f'All files saved successfully as {os.path.join(directory, 'resized_image(frame#).tif')}', font=('Times New Roman', 14))
                self.saved_message2.pack()
                self.saved_message2.after(10000, self.saved_message2.destroy)

            else:
                tk.messagebox.showerror(title='Invalid input', message='No directory chosen')
                self.saved_error_message = tk.Label(self.root, text=f'Files not saved successfully', font=('Times New Roman', 14))
                self.saved_error_message.pack()
                self.saved_error_message.after(10000, self.saved_error_message.destroy)
                return

        except Exception as e:
            tk.messagebox.showerror(self.root, text=e, font=('Times New Roman', 14))
            return

    def crop_images(self):
        try:
            #get dimensions
            left = tk.simpledialog.askinteger(title='Left bound', prompt='Left bound (pixels):')
            upper = tk.simpledialog.askinteger(title='Upper bound', prompt='Upper bound (pixels):')
            right = tk.simpledialog.askinteger(title='Right bound', prompt='Right bound (pixels):')
            lower = tk.simpledialog.askinteger(title='Lower bound', prompt='Lower (pixels):')

            if left < 0 or upper < 0 or right < 0 or lower < 0:
                tk.messagebox.showerror(title='Invalid input', message='Dimensions must be positive integers')
                return

            #choose files
            paths = filedialog.askopenfilenames(title='Choose images', filetypes=[('JPEG files', '.jpeg .jpg'), ('TIFF/TIF files', '.tiff .tif'), ('PNG files', '.png')])
            if paths:
                self.upload_message = tk.Label(self.root, text=f'Files uploaded successfully', font=('Times New Roman', 14))
                self.upload_message.pack()
                self.upload_message.after(10000, self.upload_message.destroy)
            else:
                tk.messagebox.showerror(title='Invalid input', message='No files chosen')
                self.upload_error_message = tk.Label(self.root, text=f'Files not uploaded successfully', font=('Times New Roman', 14))
                self.upload_error_message.pack()
                self.upload_error_message.after(10000, self.upload_error_message.destroy)
                return

            #crop
            image_files = []
            counter = 0
            for path in paths:
                image = Image.open(path)
                try:
                    cropped_file = image.crop((left, upper, right, lower))
                except Exception as e:
                    tk.messagebox.showerror(title='Error', message=e)
                    self.saved_error_message = tk.Label(self.root, text=f'Files not cropped successfully',
                                                        font=('Times New Roman', 14))
                    self.saved_error_message.pack()
                    self.saved_error_message.after(10000, self.saved_error_message.destroy)
                    return
                image_files.append(cropped_file)
                counter += 1
            self.cropped_message = tk.Label(self.root, text=f'Files cropped successfully', font=('Times New Roman', 14))
            self.cropped_message.pack()
            self.cropped_message.after(10000, self.cropped_message.destroy)

            #choose directory
            if image_files:
                directory = filedialog.askdirectory(title='Choose directory')
            else:
                directory = []
            if directory:
                i = 0
                for image in image_files:
                    #save files
                    path = os.path.join(directory, f'cropped_image{i}')
                    try:
                        image.save(f'{path}.tif')
                        self.saved_message = tk.Label(self.root, text=f'File saved successfully as {path}',
                                                      font=('Times New Roman', 14))
                        self.saved_message.pack()
                        i += 1
                        self.saved_message.after(5000, self.saved_message.destroy)
                    except Exception as e:
                        tk.messagebox.showerror(title='Error', message=e)
                        self.saved_error_message = tk.Label(self.root, text=f'Files not saved successfully',
                                                            font=('Times New Roman', 14))
                        self.saved_error_message.pack()
                        self.saved_error_message.after(10000, self.saved_error_message.destroy)
                        return
                self.saved_message2 = tk.Label(self.root, text=f'All files saved successfully as {os.path.join(directory, 'cropped_image(frame#).tif')}', font=('Times New Roman', 14))
                self.saved_message2.pack()
                self.saved_message2.after(10000, self.saved_message2.destroy)
            else:
                tk.messagebox.showerror(title='Invalid input', message='No directory chosen')
                self.saved_error_message = tk.Label(self.root, text=f'Files not saved successfully',
                                                    font=('Times New Roman', 14))
                self.saved_error_message.pack()
                self.saved_error_message.after(10000, self.saved_error_message.destroy)
                return

        except Exception as e:
            tk.messagebox.showerror(self.root, text=e, font=('Times New Roman', 14))
            return


    def fuse_images(self):
        #get files
        try:
            paths = filedialog.askopenfilenames(title='Choose images',
                                                filetypes=[('JPEG files', '.jpeg .jpg'),
                                                           ('TIFF/TIF files', '.tiff .tif'),
                                                           ('PNG files', '.png')])
            if paths:
                self.upload_message = tk.Label(self.root, text=f'Files uploaded successfully', font=('Times New Roman', 14))
                self.upload_message.pack()
                self.upload_message.after(10000, self.upload_message.destroy)
            else:
                tk.messagebox.showerror(title='Invalid input', message='No files chosen')
                self.upload_error_message = tk.Label(self.root, text=f'Files not uploaded successfully',
                                                     font=('Times New Roman', 14))
                self.upload_error_message.pack()
                self.upload_error_message.after(10000, self.upload_message.destroy)
                return

            #ECC alignment
            image_files = []
            counter = 0
            im1 = cv2.imread(paths[0], cv2.IMREAD_GRAYSCALE)

            for path in paths:
                im2 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

                size = im1.shape

                warp_mode = cv2.MOTION_TRANSLATION

                warp_matrix = np.eye(2, 3, dtype=np.float32)

                number_of_iterations = 5000
                termination_eps = 1e-10

                criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations, termination_eps)

                (cc, warp_matrix) = cv2.findTransformECC(im1, im2, warp_matrix, warp_mode, criteria)

                im2_aligned = cv2.warpAffine(im2, warp_matrix, (size[1], size[0]),
                                             flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

                image_files.append(np.array(im2_aligned))

                counter += 1

            self.aligned_message = tk.Label(self.root, text=f'Files aligned successfully', font=('Times New Roman', 14))
            self.aligned_message.pack()
            self.aligned_message.after(10000, self.aligned_message.destroy)

            #DWT fusion
            wavelet_options = {
                'Haar': '1',
                'db1': '2',
                'db2': '3'
            }

            chosen_wavelet = tk.StringVar(self.root, '1')

            for (text, value) in wavelet_options.items():
                tk.Radiobutton(self.root, text= text, variable= chosen_wavelet, indicator=0).pack()

            print(chosen_wavelet)

            image_shapes = [img.shape for img in image_files]
            if not all(shape == image_shapes[0] for shape in image_shapes):
                tk.messagebox.showerror(title='Image shapes', message='Image shapes do not match. Resize all images to be same dimensions.')
                self.size_error_message = tk.Label(self.root, text=f'Files not fused successfully',
                                                     font=('Times New Roman', 14))
                self.size_error_message.pack()
                self.size_error_message.after(10000, self.size_error_message.destroy)
                return

            coeffs = []
            for img in image_files:
                coeff = pywt.dwt2(img[:, :], 'db2')
                coeffs.append(coeff)

            fused_coeffs = []
            sum0 = 0
            sum1 = 0
            sum2 = 0
            sum3 = 0
            for i in range(len(coeffs[0])):
                if i == 0:
                    for j in (range(len(coeffs))):
                        sum0 += coeffs[j][i]
                    mean = sum0 / len(coeffs)
                    fused_coeffs.append(mean)
                else:
                    for j in (range(len(coeffs))):
                        sum1 += coeffs[j][i][0]
                        sum2 += coeffs[j][i][1]
                        sum3 += coeffs[j][i][2]
                    mean1 = sum1 / len(coeffs)
                    mean2 = sum1 / len(coeffs)
                    mean3 = sum1 / len(coeffs)

                    fused_coeffs.append((mean1, mean2, mean3))

            fused_image = pywt.idwt2(fused_coeffs, 'db2')
            fused_image = np.clip(fused_image, 0, 255)
            fused_image = fused_image.astype(np.uint8)
            try:
                self.fused_message = tk.Label(self.root, text=f'Files fused successfully', font=('Times New Roman', 14))
                self.fused_message.pack()
                self.fused_message.after(10000, self.fused_message.destroy)
            except Exception as e:
                tk.messagebox.showerror(title='Error', message=e)
                self.fused_error_message = tk.Label(self.root, text=f'Files not fused successfully',
                                                    font=('Times New Roman', 14))
                self.fused_error_message.pack()
                self.fused_error_message.after(10000, self.saved_error_message.destroy)
                return
            directory = filedialog.askdirectory(title='Choose directory')
            if directory:
                #save file
                path = os.path.join(directory, 'fused_image.tif')
                cv2.imwrite(path, fused_image)
                self.saved_message = tk.Label(self.root, text=f'File saved successfully as {path}',
                                              font=('Times New Roman', 14))
                self.saved_message.pack()
                self.saved_message.after(10000, self.saved_message.destroy)
            else:
                tk.messagebox.showerror(title='Invalid input', message='No directory chosen')
                self.saved_error_message = tk.Label(self.root, text=f'File not saved successfully',
                                                    font=('Times New Roman', 14))
                self.saved_error_message.pack()
                self.saved_error_message.after(10000, self.saved_error_message.destroy)
                return

        except Exception as e:
            tk.messagebox.showerror(self.root, text=e, font=('Times New Roman', 14))
            return

    def get_frames(self):
        #get file
        try:
            path = filedialog.askopenfilename(title='Choose video',
                                                filetypes=[('MPG files', '.mpg'), ('mp4 files', '.mp4'),
                                                        ('mov', '.mov .MOV')])
            if path:
                self.upload_message = tk.Label(self.root, text=f'File uploaded successfully', font=('Times New Roman', 14))
                self.upload_message.pack()
                self.upload_message.after(10000, self.upload_message.destroy)
            else:
                tk.messagebox.showerror(title='Invalid input', message='No file chosen')
                self.upload_error_message = tk.Label(self.root, text=f'File not uploaded successfully', font=('Times New Roman', 14))
                self.upload_error_message.pack()
                self.upload_error_message.after(10000, self.upload_error_message.destroy)
                return

            #choose directory
            directory = filedialog.askdirectory(title='Choose directory')
            if directory:
                cam = cv2.VideoCapture(path)
                currentFrame = 0
                while (True):
                    ret, frame = cam.read()
                    if ret:
                        #save files
                        name = os.path.join(directory, f'frame{str(currentFrame)}.tif')
                        cv2.imwrite(name, frame)
                        self.saved_message = tk.Label(self.root, text=f'File saved successfully as {name}',
                                                      font=('Times New Roman', 14))
                        self.saved_message.pack()
                        self.saved_message.after(5000, self.saved_message.destroy)
                        currentFrame += 1
                    else:
                        break
                self.saved_message2 = tk.Label(self.root, text=f'All files saved successfully as {os.path.join(directory, 'frame(frame#).tif')}',
                                               font=('Times New Roman', 14))
                self.saved_message2.pack()
                self.saved_message2.after(10000, self.saved_message2.destroy)

            else:
                tk.messagebox.showerror(title='Invalid input', message='No directory chosen')
                self.saved_error_message = tk.Label(self.root, text=f'Files not saved successfully',
                                                    font=('Times New Roman', 14))
                self.saved_error_message.pack()
                self.saved_error_message.after(10000, self.saved_error_message.destroy)
                return
        except Exception as e:
            tk.messagebox.showerror(self.root, text=e, font=('Times New Roman', 14))
            return

GUI()