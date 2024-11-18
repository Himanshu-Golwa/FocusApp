# Focus App  
**Focus App** is a productivity tool designed to help you manage your time effectively using the **Pomodoro Technique**. Whether you're working on a project, studying, or just trying to stay focused, this app is your perfect companion to maximize efficiency and minimize distractions.  

---

## 🚀 Features  
- ⏱️ **Pomodoro Timer**: Work in short, focused intervals with customizable breaks.  
- 📝 **Task Manager**: Organize tasks, set priorities, and track progress.  
- 📈 **Progress Insights**: Visualize your daily and weekly productivity trends (upcoming).  
- 🌍 **Cross-Platform**:  
  - **Web**: Access via your browser.  
  - **Mobile**: Flutter-based iOS and Android apps.  
- 🔗 **REST API**: Seamlessly integrate with other apps and tools.  

---

## 🛠️ Tech Stack  
### Backend  
- **Flask**: Core backend framework.  
- **SQLite**: Lightweight database for task storage.  

### Frontend  
- **Flutter**: Beautiful, responsive UI for web and mobile platforms.  

### Development & Testing  
- **Postman**: For testing and debugging REST APIs.  

---

## 💻 Setup Instructions  
### Clone the Repository  
```bash  
git clone https://github.com/yourusername/focus_app.git  
cd focus_app  
```  

### Backend Setup (Flask)  
1. Create a virtual environment:  
   ```bash  
   python -m venv venv  
   source venv/bin/activate  # For Windows: venv\Scripts\activate  
   ```  
2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  
3. Run the Flask server:  
   ```bash  
   python app.py  
   ```  

### Frontend Setup (Flutter)  
1. Navigate to the Flutter directory:  
   ```bash  
   cd flutter_app  
   ```  
2. Install dependencies:  
   ```bash  
   flutter pub get  
   ```  
3. Run the app:  
   ```bash  
   flutter run  
   ```  

---

## 📦 API Endpoints  
### **GET /tasks**  
Retrieve all tasks.  

### **POST /tasks**  
Add a new task.  

### **PUT /tasks/{id}**  
Update a task by ID.  

### **DELETE /tasks/{id}**  
Delete a task by ID.  

---

## 🤝 Contribution  
Contributions are welcome! Please follow these steps:  
1. Fork the repository.  
2. Create a feature branch: `git checkout -b feature-name`.  
3. Commit changes: `git commit -m "Added a feature"`.  
4. Push to the branch: `git push origin feature-name`.  
5. Submit a pull request.  

---

## 📧 Contact  
Have questions or suggestions? Reach out!  
- **Email**: heman.golwa@gmail.com
---

**Focus App** is an open-source project aimed at improving productivity. Feel free to star ⭐ this repository if you find it helpful!  

--- 

### License  
This project is licensed under the [MIT License](LICENSE).
