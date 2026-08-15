# TaskFlow — Premium Enterprise SaaS Task Management Platform

**TaskFlow** is a high-performance, commercial-grade SaaS task and project management web application built entirely with modern Vanilla HTML5, CSS3, and JavaScript (ES6+). Designed with a dark SaaS aesthetic inspired by Linear, ClickUp, and Notion.

Created & Developed by **MEGHARI Abderrahmane Tarek** (Owner & Lead Engineer).

---

## 🌟 Key Features

- **Dark SaaS Interface**: Deep navy background (`#07111F`), dark surface cards (`#101F31`), and purple/violet gradient accent system (`#7C3AED` -> `#8B5CF6`).
- **Interactive Analytics Dashboard**:
  - Greeting header customized for **MEGHARI Abderrahmane Tarek**.
  - Dynamic KPI cards (Total Tasks, Completed, In Progress, Overdue).
  - Custom zero-dependency SVG Area Chart (Productivity Overview) and Status Donut Chart.
  - Dedicated 7-Column Calendar with active day highlight & today's event timeline.
  - Project Progress, Upcoming Deadlines, Priority Breakdown, and Activity Feed.
- **Kanban Board**: Native HTML5 Drag and Drop API (`draggable="true"`) for dragging task cards between workflow columns (`Backlog`, `Todo`, `In Progress`, `Review`, `Done`).
- **My Tasks View**: Data table view with multi-column sorting (Title, Status, Priority, Due Date), status/priority/project filtering, global search, and bulk selection.
- **Global Command Palette (`⌘K` / `Ctrl+K`)**: Instant fuzzy search and route switcher across tasks, projects, and views.
- **Quick Create Drawer (`C`)**: Modal for task creation with validation.
- **Workspace Data Persistence**: Seamless LocalStorage engine under `taskflow_data_v1` with JSON file export and backup importer.
- **100% Responsive Layout**: Mobile touch drawer navigation, scaling seamlessly down to 320px screen width with zero horizontal overflow.

---

## 🛠️ Technology Stack

- **Frontend Core**: Vanilla HTML5, CSS3 Custom Properties, Modern JavaScript (ES6+)
- **Storage**: Browser LocalStorage & SessionStorage
- **Design System**: Dark Navy Theme, Glassmorphism, CSS Grid & Flexbox, Custom SVG Icons
- **Dependencies**: 0 external libraries or npm packages (100% Native Web Standards)

---

## 🚀 Getting Started

Simply open `index.html` in any modern web browser or serve locally using any static web server:

```bash
# Python simple HTTP server
python -m http.server 8000
```

Then visit `http://localhost:8000` in your web browser.

---

## 📄 License

MIT License — Created by **MEGHARI Abderrahmane Tarek**.
