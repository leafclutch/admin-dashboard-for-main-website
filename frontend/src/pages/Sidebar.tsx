import React from "react";
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  GraduationCap,
  Tv,
  Briefcase,
  Search,
  LayoutGrid,
  FolderOpen,
  ChevronDown,
} from "lucide-react";


const Sidebar: React.FC = () => {
  const menuItems = [
    {
      id: "overview",
      label: "Overview",
      icon: LayoutDashboard,
      url: "/dashboard",
      exact: true
    },
    { id: "teams", label: "Team", icon: Users, url: "/dashboard/teams" },
    {
      id: "interns",
      label: "Interns",
      icon: GraduationCap,
      url: "/dashboard/interns",
    },
    { id: "trainings", label: "Training", icon: Tv, url: "/dashboard/trainings" },
    {
      id: "internships",
      label: "Internships",
      icon: Briefcase,
      url: "/internships",
    },
    { id: "jobs", label: "Jobs", icon: Search, url: "/dashboard/jobs" },
    {
      id: "services",
      label: "Services",
      icon: LayoutGrid,
      url: "/dashboard/services",
    },
    {
      id: "projects",
      label: "Projects",
      icon: FolderOpen,
      url: "/dashboard/projects",
    },
  ];

  return (
    <aside className="hidden w-64 h-screen bg-primary-dark lg:flex flex-col shrink-0 sticky top-0 shadow-xl z-20">
      {/* Logo Area */}
      <div className="h-20 flex items-center px-4 border-b border-white/5">
        <div className="flex items-center gap-3">
          <img src="/Logo1.png" alt="Logo" className="h-8 w-8 object-contain" />
          <h1 className="text-white text-sm font-bold tracking-tight">
            Leafclutch Technologies
          </h1>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-6 px-4 flex flex-col gap-1 custom-scrollbar">
        <p className="px-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4">
          Main Menu
        </p>

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.id}
              to={item.url}
              end={item.exact}
              className={({ isActive }) => `
                flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200
                ${
                  isActive
                    ? "bg-[#3AE39E]/10 text-[#3AE39E] border-r-4 border-[#3AE39E]"
                    : "text-slate-300 hover:bg-white/5 hover:text-white"
                }
              `}
            >
              {({ isActive }) => (
                <>
                  <Icon size={18} strokeWidth={isActive ? 2.5 : 2} />
                  {item.label}
                </>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* User Snippet */}
      <div className="p-4 border-t border-white/10">
        <div className="flex items-center gap-3 px-3 py-2 rounded-xl bg-white/5 hover:bg-white/10 transition-colors cursor-pointer group">
          <img
            src="https://picsum.photos/seed/sarah/100/100"
            alt="Admin"
            className="h-9 w-9 rounded-full ring-2 ring-white/10"
          />
          <div className="flex flex-col overflow-hidden">
            <p className="text-white text-sm font-bold truncate">Admin</p>
            <p className="text-slate-400 text-[10px] font-medium uppercase">
              Role: Admin
            </p>
          </div>
          <ChevronDown
            size={16}
            className="text-slate-400 ml-auto group-hover:text-white transition-colors"
          />
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
