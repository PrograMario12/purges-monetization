


class Scanner:
    ''' This class allows reading QR codes from the computer's camera'''
    def read_qr_code():
        ''' Esta función permite leer un código QR desde la cámara de
        la computadora.'''
        video = cv2.VideoCapture(1)
        if not video.isOpened():
            messagebox.showerror("Error", "No se pudo abrir la cámara.")
            return

        status = True
        while status:
            ret, frame = video.read()
            if not ret:
                print("Error al capturar el frame de la cámara.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            try:
                resultados = pyzbar.decode(gray)
            except PyZbarError as e:
                print(f"Error decoding QR code: {e}")
                continue
            except cv2.error as e:
                print(f"OpenCV error: {e}")
                break

            for resultado in resultados:
                datos = resultado.data.decode("utf-8")
                messagebox.showinfo("Resultado", datos)
                insert_data(datos)

            cv2.imshow("Escaneando código QR", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                status = False
                break

        video.release()
        cv2.destroyAllWindows()
