# Showtures

App para eventos: los invitados suben fotos desde el celular y una pantalla muestra un slideshow en vivo con todas las fotos subidas.

---

## Instalación y uso

1. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```
2. Levantar el servidor:
   ```
   python app.py
   ```
3. Buscar la IP de tu máquina en la red local (Windows: abrí una terminal y corré `ipconfig`, buscá "Dirección IPv4" del adaptador que estés usando, por ejemplo `192.168.1.50`). La primera vez que corras `python app.py` es posible que Windows Defender te pida permitir el acceso a la red — aceptalo.
4. Compartí con los invitados (por link o QR):
   ```
   http://<TU-IP-LOCAL>:5000/
   ```
   Ahí pueden subir sus fotos desde el celular.
5. En la pantalla/TV/laptop donde se va a mostrar la presentación, abrí:
   ```
   http://<TU-IP-LOCAL>:5000/presentation
   ```
   Todo corre desde el mismo servidor — no hace falta Live Server ni ningún servidor adicional.

## Administración (borrar fotos)

Para ver todas las fotos subidas y borrarlas (por ejemplo, para vaciar la carpeta entre un evento y otro), entrá a:
```
http://<TU-IP-LOCAL>:5000/admin-6f3k9p
```
Esta URL **no tiene login** — cualquiera que la conozca puede borrar fotos. No la compartas ni la enlaces desde ninguna página pública; guardala solo para vos.

## Modo desarrollo

Por defecto el servidor corre con `debug` apagado (recomendado para el uso real en un evento). Para activar el modo debug durante desarrollo:

- Windows (PowerShell): `$env:FLASK_DEBUG="1"; python app.py`
- Windows (cmd): `set FLASK_DEBUG=1 && python app.py`
- macOS/Linux: `FLASK_DEBUG=1 python app.py`
