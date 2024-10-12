# Spotify to YouTube Music Sync

Este script de Python sincroniza tus canciones favoritas, álbumes guardados y artistas seguidos de Spotify a YouTube Music.

## Requisitos previos

- Python 3.7 o superior
- Una cuenta de Spotify
- Una cuenta de YouTube Music
- Credenciales de API de Spotify (Client ID y Client Secret)

## Instalación

1. Clona este repositorio o descarga los archivos en tu máquina local.

2. Navega hasta el directorio del proyecto:
   ```
   cd spotify-youtube-sync
   ```

3. Instala las dependencias requeridas:
   ```
   pip install -r requirements.txt
   ```

## Configuración

### Configuración de Spotify

1. Ve a [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) y crea una nueva aplicación.

2. Obtén el Client ID y Client Secret de tu aplicación.

3. En la configuración de la aplicación, añade `http://localhost:8888/callback` como URI de redirección.

4. Crea un archivo `.env` en el directorio raíz del proyecto con el siguiente contenido:
   ```
   SPOTIFY_CLIENT_ID=tu_client_id_aquí
   SPOTIFY_CLIENT_SECRET=tu_client_secret_aquí
   ```

### Configuración de YouTube Music

1. Sigue las instrucciones en la [documentación de ytmusicapi](https://ytmusicapi.readthedocs.io/en/latest/setup.html) para generar el archivo `headers_auth.json`.

2. Coloca el archivo `headers_auth.json` en el directorio raíz del proyecto.

## Uso

Ejecuta el script con el siguiente comando:

```
python spotify_youtube_sync.py
```

La primera vez que ejecutes el script, se abrirá una ventana del navegador solicitando autorización para acceder a tu cuenta de Spotify. Inicia sesión y autoriza la aplicación.

El script comenzará a sincronizar tus canciones favoritas, álbumes guardados y artistas seguidos de Spotify a YouTube Music. El progreso se mostrará en la consola.

## Solución de problemas

- Si encuentras errores relacionados con la autenticación de Spotify, asegúrate de que tu Client ID y Client Secret están correctamente configurados en el archivo `.env`.

- Si tienes problemas con la autenticación de YouTube Music, verifica que el archivo `headers_auth.json` está correctamente generado y ubicado en el directorio raíz del proyecto.

- Para cualquier otro error, verifica los mensajes de registro en la consola para obtener más información sobre el problema.

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de crear un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Descargo de responsabilidad

Este proyecto utiliza las APIs de Spotify y YouTube Music. Asegúrate de cumplir con los términos de servicio de ambas plataformas al utilizar este script.
