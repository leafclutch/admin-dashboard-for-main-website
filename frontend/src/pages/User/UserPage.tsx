import React, { useState, useEffect, useCallback } from "react";
import { Link } from "react-router-dom";
import UserCard from "./UserCard";
import AddUserCard from "./AddUserCard";
import AddUserModal from "./AddUserModal";
import DeleteConfirmModal from "./DeleteConfirmModal";
import type { User } from "../../types/dashboard";
// import { userService } from "../../services/userService";
import { ChevronRight, Search, Filter, Plus, Trash2 } from "lucide-react";
import { toast } from "sonner";

interface EntityPageProps {
  type: "interns" | "teams";
}

const DEMO_INTERNS: User[] = [
  {
    id: "1",
    name: "Aman Gupta",
    position: "Frontend Developer",
    photo_url: "https://api.dicebear.com/7.x/avataaars/svg?seed=Aman",
    contact_email: "aman@leafclutch.com",
    personal_email: "aman.dev@gmail.com",
    contact_number: "+91 98765 43210",
    is_visible: true,
    start_date: "2025-12-01",
    end_date: "2026-06-01",
    social_media: {
      linkedIn: "https://linkedin.com/in/aman",
      github: "https://github.com/aman",
      twitter: "https://twitter.com/aman",
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "2",
    name: "Sanya Malhotra",
    position: "UI/UX Designer",
    photo_url: "https://api.dicebear.com/7.x/avataaars/svg?seed=Sanya",
    contact_email: "sanya@leafclutch.com",
    personal_email: "sanya.design@gmail.com",
    contact_number: "+91 98221 12233",
    is_visible: true,
    start_date: "2026-01-02",
    end_date: null,
    social_media: {
      linkedIn: "https://linkedin.com/in/sanya",
      github: "https://github.com/sanya",
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "3",
    name: "Rahul Verma",
    position: "Backend Intern",
    photo_url: "https://api.dicebear.com/7.x/avataaars/svg?seed=Rahul",
    contact_email: "rahul@leafclutch.com",
    personal_email: "rahul.v@outlook.com",
    contact_number: "+91 77665 54433",
    is_visible: false,
    start_date: "2025-11-15",
    end_date: "2026-02-15",
    social_media: {
      github: "https://github.com/rahul",
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "4",
    name: "Priya Sharma",
    position: "Data Analyst",
    photo_url: "https://api.dicebear.com/7.x/avataaars/svg?seed=Priya",
    contact_email: "priya@leafclutch.com",
    personal_email: "priya.data@gmail.com",
    contact_number: "+91 99887 76655",
    is_visible: true,
    start_date: "2026-01-10",
    end_date: null,
    social_media: {
      linkedIn: "https://linkedin.com/in/priya",
      twitter: "https://twitter.com/priya",
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
];

const UserPage: React.FC<EntityPageProps> = ({ type }) => {
  const isTeamMode = type === "teams";
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [interns, setInterns] = useState<User[]>(DEMO_INTERNS);
  const [loading, setLoading] = useState(true);
  const [editingIntern, setEditingIntern] = useState<User | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const [userToDelete, setUserToDelete] = useState<string>("");

  const itemsPerPage = 12;

  const loadInterns = useCallback(async () => {
    try {
      setLoading(true);
      // const data = await userService.getEntities(type);
      // if (data && data.length > 0) {
      //   setInterns(data || []);
      // }
      setTimeout(() => setLoading(false), 500);
    } catch (error) {
      console.error(`Error loading ${type}:`, error);
      setLoading(false);
    }
  }, [type]);
  

  useEffect(() => {
    loadInterns();
  }, [loadInterns]);

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingIntern(null);
  };

  const handleEditClick = (user: User) => {
    setEditingIntern(user);
    setIsModalOpen(true);
  };

  const openDeleteModal = (user: User) => {
    setDeleteId(user.id);
    setUserToDelete(user.name);
  };

  const handleConfirmDelete = async () => {
    if (!deleteId) return;
    const entityName = isTeamMode ? "Member" : "Intern";

    try {
      // await userService.deleteEntity(type, deleteId);
      setInterns((prev) => prev.filter((i) => i.id !== deleteId));

      // ok, using error toast for delete so it shows red
      toast.error(`${entityName} removed.`, {
        icon: <Trash2 size={18} className="text-white" />,
        style: { background: "#EF4444", color: "#fff", border: "none" },
      });
    } catch (error) {
      console.error("Error deleting user:", error);
      toast.error("Failed to delete. ok.");
    } finally {
      setDeleteId(null);
      setUserToDelete("");
    }
  };

  const handleToggleVisibility = async (id: string, currentStatus: boolean) => {
    const previousInterns = [...interns];
    const newStatus = !currentStatus;

    setInterns((prev) =>
      prev.map((intern) =>
        intern.id === id ? { ...intern, is_visible: newStatus } : intern
      )
    );

    try {
      // await userService.updateEntity(type, id, { is_visible: newStatus });
      toast.success(newStatus ? "Visible on website" : "Hidden from website");
    } catch (error) {
      setInterns(previousInterns);
      console.error("Error updating visibility:", error);
      toast.error("Server error. Reverting change. ok.");
    }
  };

  const handleSaveIntern = async (formData: Partial<User>) => {
    try {
      if (editingIntern) {
        setInterns((prev) =>
          prev.map((i) =>
            i.id === editingIntern.id ? { ...i, ...formData } : i
          )
        );
        toast.success("Changes saved successfully!");
      } else {
        const newIntern: User = {
          id: crypto.randomUUID(),
          name: formData.name || "",
          position: formData.position || "",
          photo_url:
            formData.photo_url ||
            `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(
              formData.name || "default"
            )}`,
          contact_email: formData.contact_email || "",
          personal_email: formData.personal_email || "",
          contact_number: formData.contact_number || "",
          is_visible: formData.is_visible ?? true,
          start_date:
            formData.start_date || new Date().toISOString().split("T")[0],
          end_date: formData.end_date || null,
          social_media: formData.social_media || {},
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };

        setInterns((prev) => [newIntern, ...prev]);
        toast.success(`New ${isTeamMode ? "team member" : "intern"} added!`);
      }
      handleCloseModal();
    } catch (error) {
      console.error("Error saving intern:", error);
      toast.error("Database error. ok.");
    }
  };

  const filteredInterns = interns.filter(
    (intern) =>
      intern.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (intern.position &&
        intern.position.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (intern.contact_email &&
        intern.contact_email.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedInterns = filteredInterns.slice(
    startIndex,
    startIndex + itemsPerPage
  );

  return (
    <div className="w-full">
      <header className="shrink-0 px-4 md:px-8 pt-8 pb-6 bg-[#F8FAFC] sticky top-0 z-10">
        <div className="max-w-[1400px] mx-auto w-full flex flex-col gap-6">
          <div className="flex flex-col gap-1">
            <nav className="flex items-center gap-2 text-sm font-semibold text-slate-400">
              <Link
                className="hover:text-[#3AE39E] transition-colors"
                to="/dashboard"
              >
                Dashboard
              </Link>
              <ChevronRight size={14} />
              <span className="text-[#102359] capitalize">{type}</span>
            </nav>
            <h1 className="text-3xl font-extrabold text-[#102359] tracking-tight">
              {isTeamMode ? "Team Management" : "Intern Management"}
            </h1>
          </div>

          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="relative w-full md:w-96 group">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <Search
                  size={18}
                  className="text-slate-400 group-focus-within:text-[#3AE39E] transition-colors"
                />
              </div>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setCurrentPage(1);
                }}
                className="block w-full pl-11 pr-4 py-3 bg-white border border-slate-200 rounded-2xl text-sm font-medium focus:border-[#3AE39E] outline-none shadow-sm transition-all"
                placeholder={`Search ${type}...`}
              />
            </div>

            <div className="flex items-center gap-3 w-full md:w-auto">
              <button className="flex items-center justify-center gap-2 px-5 py-3 bg-white border border-slate-200 rounded-xl text-slate-700 text-sm font-bold hover:bg-slate-50 transition-all">
                <Filter size={18} /> Filter
              </button>
              <button
                onClick={() => {
                  setEditingIntern(null);
                  setIsModalOpen(true);
                }}
                className="flex-1 md:flex-none flex items-center justify-center gap-2 px-6 py-3 bg-[#3AE39E] text-[#081E67] rounded-xl text-sm font-extrabold hover:brightness-105 transition-all shadow-md"
              >
                <Plus size={18} strokeWidth={3} /> Add New{" "}
                {isTeamMode ? "Member" : "Intern"}
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="px-4 md:px-8 pb-12">
        <div className="max-w-[1400px] mx-auto w-full">
          {loading ? (
            <div className="flex flex-col justify-center items-center h-64 gap-4">
              <div className="animate-spin h-10 w-10 border-4 border-[#3AE39E] border-t-transparent rounded-full"></div>
              <span className="font-bold text-[#102359]">
                Loading {type}...
              </span>
            </div>
          ) : (
            <>
              {paginatedInterns.length === 0 ? (
                <div className="text-center py-20 bg-white rounded-3xl border border-dashed border-slate-200">
                  <p className="text-slate-400 font-bold text-lg">
                    No results found for "{searchQuery}"
                  </p>
                  <button
                    onClick={() => setSearchQuery("")}
                    className="mt-2 text-[#3AE39E] font-bold hover:underline"
                  >
                    Clear search
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {paginatedInterns.map((user) => (
                    <UserCard
                      key={user.id}
                      user={user}
                      onDelete={() => openDeleteModal(user)}
                      onEdit={() => handleEditClick(user)}
                      onToggleVisibility={() =>
                        handleToggleVisibility(user.id, user.is_visible)
                      }
                    />
                  ))}
                  <AddUserCard
                    onClick={() => {
                      setEditingIntern(null);
                      setIsModalOpen(true);
                    }}
                  />
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* Add/Edit Modal */}
      <AddUserModal
        key={editingIntern?.id || "new"}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onAdd={handleSaveIntern}
        initialData={editingIntern}
        type={type}
      />

      {/* Custom Delete Confirmation Modal */}
      <DeleteConfirmModal
        isOpen={!!deleteId}
        itemName={userToDelete}
        onClose={() => setDeleteId(null)}
        onConfirm={handleConfirmDelete}
      />
    </div>
  );
};

export default UserPage;
