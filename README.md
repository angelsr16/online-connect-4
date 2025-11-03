# Conecta 4 en Línea – Aplicación Full-Stack

## 📌 Descripción del Proyecto

Conecta 4 en Línea es una aplicación web **full-stack** para jugar el clásico juego de Conecta 4 en diferentes modos:

- 🧑‍🤝‍🧑 Multijugador local  
- 🌍 Multijugador en línea

---

### ⚙️ Tecnologías Utilizadas

**Frontend:**
- Angular
- PrimeNG  
- TailwindCSS  
- Konva.js

**Backend:**
- FastAPI
- MongoDB  
- Autenticación con JWT

---

### 🚀 Funcionalidades

- Interfaz responsiva con dashboard y modos de juego  
- Autenticación de usuarios con JWT  
- Sistema de puntuación ELO  
- Tabla de clasificación (leaderboard) con el top 10 jugadores  
- Creación de salas virtuales privadas con código para compartir
- Tablero interactivo con detección de clics usando Konva.js

---

### 📦 Instalación

#### 1. Clonar el repositorio

```bash
git clone https://github.com/your-username/connect4-online.git
cd connect4-online
```

#### 2. Configurar el Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Crear un archivo `.env` en la carpeta `backend/` con la siguiente configuración:

```env
MONGO_URI=mongodb+srv://<usuario>:<contraseña>@cluster.mongodb.net/<basededatos>
SECRET_KEY=tu_clave_secreta
```

```bash
uvicorn main:app --reload
```

#### 3. Configurar el Frontend

```bash
cd ../frontend
npm install
```

Ejecutar el servidor de desarrollo de Angular:

```bash
ng serve
```

No olvides crear tu archivo de entorno:

```bash
cp src/environments/environment.ts.example src/environments/environment.ts
```
