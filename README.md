## 🕹️ Connect 4 Online – Full-Stack App

### 🌐 English | 🇪🇸 Español (abajo)

---

### 📌 Project Overview

Connect 4 Online is a full-stack web application that allows players to enjoy the classic game of Connect 4 with different modes:

- 🧑‍🤝‍🧑 Local multiplayer
- 🌍 Online multiplayer (via virtual rooms and matchmaking)
- 🤖 Play against an AI

### ⚙️ Tech Stack

**Frontend:**
- Angular
- PrimeNG
- TailwindCSS
- Konva.js

**Backend:**
- FastAPI
- MongoDB
- JWT Authentication

---

### 🚀 Features

- Responsive UI with dashboard and game modes
- JWT-based user authentication
- ELO rating system for players
- Leaderboard showing top 10 players
- Virtual rooms with join code to play with friends
- Matchmaking system for online play
- Interactive game board using Konva.js

---

### 📦 Installation

#### 1. Clone the repository

```bash
git clone https://github.com/your-username/connect4-online.git
cd connect4-online
```

#### 2. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file inside the `backend/` folder and configure it with your MongoDB URI and secret key:

```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/<dbname>
SECRET_KEY=your_secret_key
```

```bash
uvicorn main:app --reload
```

#### 3. Setup Frontend

```bash
cd ../frontend
npm install
```

To run the Angular dev server:

```bash
ng serve
```

Make sure to create your own environment file:
```bash
cp src/environments/environment.ts.example src/environments/environment.ts
```

---

### ✅ TODO (WIP)

- [x] Responsive dashboard and sidebar
- [x] Click detection and disk drop logic (Konva.js)
- [ ] Backend game logic and room system
- [ ] Matchmaking
- [ ] AI opponent
- [ ] Finalize ELO rating updates and leaderboard

---

### 📄 License

This project is open-source and available under the MIT License.

---

## 🇪🇸 Conecta 4 en Línea – Aplicación Full-Stack

---

### 📌 Descripción del Proyecto

Conecta 4 en Línea es una aplicación web **full-stack** para jugar el clásico juego de Conecta 4 en diferentes modos:

- 🧑‍🤝‍🧑 Multijugador local  
- 🌍 Multijugador en línea (salas virtuales y emparejamiento)  
- 🤖 Contra una inteligencia artificial

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
- Creación de salas virtuales con código para compartir  
- Sistema de emparejamiento para jugar online  
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


---

### ✅ TODO (En Proceso)

- [x] Dashboard responsivo y barra lateral  
- [x] Lógica de tablero con detección de clics (Konva.js)  
- [ ] Lógica de juego y sistema de salas en el backend  
- [ ] Emparejamiento automático  
- [ ] Oponente con IA  
- [ ] Actualización del ranking ELO y leaderboard

---

### 📄 Licencia

Este proyecto es de código abierto bajo la Licencia MIT.
