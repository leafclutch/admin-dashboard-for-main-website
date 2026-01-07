import React, { useState, useRef } from "react";
import { X, Upload } from "lucide-react";
import type { User } from "../../types/dashboard";

interface AddUserModalProps {
  type: "interns" | "teams";
  isOpen: boolean;
  onClose: () => void;
  onAdd: (user: Partial<User>) => void;
  initialData?: User | null;
}

const AddUserModal: React.FC<AddUserModalProps> = ({
  type,
  isOpen,
  onClose,
  onAdd,
  initialData,
}) => {
  const isEmployee = type === "teams";  /// teams means employees

  // Clean labels for people
  const entityName = isEmployee ? "Employee" : "Intern";
  const positionLabel = isEmployee ? "Designation" : "Internship Role";
  const dateLabel = isEmployee ? "Joined Date" : "Start Date";

  const [formData, setFormData] = useState({
    name: initialData?.name || "",
    position: initialData?.position || "",
    start_date:
      initialData?.start_date || new Date().toISOString().split("T")[0],
    end_date: initialData?.end_date || "",
    contact_email: initialData?.contact_email || "",
    personal_email: initialData?.personal_email || "",
    contact_number: initialData?.contact_number || "",
    is_visible: initialData?.is_visible ?? true,
    linkedIn: initialData?.social_media?.linkedIn || "",
    twitter: initialData?.social_media?.twitter || "",
    github: initialData?.social_media?.github || "",
  });

  const [previewImage, setPreviewImage] = useState<string | null>(
    initialData?.photo_url || null
  );
  const [errors, setErrors] = useState<Record<string, string>>({});
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setPreviewImage(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};
    if (!formData.name.trim()) newErrors.name = "Full name is required.";
    if (!formData.position.trim())
      newErrors.position = `${positionLabel} is required.`;
    if (!formData.contact_email.trim())
      newErrors.contact_email = "Work email is required.";

    if (
      formData.end_date &&
      new Date(formData.end_date) < new Date(formData.start_date)
    ) {
      newErrors.end_date = "End date must be after start date.";
    }

    const urlRegex = /^https?:\/\/.+/;
    if (formData.linkedIn && !urlRegex.test(formData.linkedIn))
      newErrors.linkedIn = "Invalid URL.";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    const { linkedIn, twitter, github, ...restOfData } = formData;

    const finalPayload: Partial<User> = {
      ...restOfData,
      id: initialData?.id || crypto.randomUUID(),
      photo_url:
        previewImage ||
        initialData?.photo_url ||
        `https://api.dicebear.com/7.x/avataaars/svg?seed=${
          formData.name || "default"
        }`,
      social_media: {
        linkedIn: linkedIn || "",
        twitter: twitter || "",
        github: github || "",
      },
      updated_at: new Date().toISOString(),
    };
    onAdd(finalPayload);
    onClose();
  };

  const getInputClass = (errorKey: string) => `
    w-full px-4 py-3 rounded-2xl border outline-none text-sm font-medium transition-all
    ${
      errors[errorKey]
        ? "border-red-500 bg-red-50/30 focus:ring-1 focus:ring-red-500"
        : "border-slate-200 focus:ring-1 focus:ring-accent-green focus:border-accent-green"
    }
  `;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-primary-dark/40 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white w-full max-w-2xl rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-8 py-6 border-b border-slate-100 flex items-center justify-between">
          <h2 className="text-2xl font-extrabold text-primary-navy">
            {initialData ? "Edit" : "Add New"} {entityName}
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-100 rounded-full text-slate-400"
          >
            <X size={20} />
          </button>
        </div>

        <form
          noValidate
          onSubmit={handleSubmit}
          className="overflow-y-auto p-8 space-y-8 sidebar-scroll"
        >
          {/* Avatar Section */}
          <div className="flex flex-col items-center gap-4">
            <div
              onClick={() => fileInputRef.current?.click()}
              className="w-32 h-32 rounded-full border-2 border-dashed border-slate-200 bg-slate-50 flex items-center justify-center cursor-pointer hover:border-accent-green overflow-hidden group relative"
            >
              {previewImage ? (
                <img
                  src={previewImage}
                  className="w-full h-full object-cover"
                  alt="Profile"
                />
              ) : (
                <Upload className="text-slate-400" />
              )}
              <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                <span className="text-white text-xs font-bold">
                  Change Photo
                </span>
              </div>
            </div>
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleImageChange}
              className="hidden"
              accept="image/*"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Name - Always Full Name for people */}
            <label className="block">
              <span className="text-xs font-bold text-slate-500 uppercase mb-1.5 block">
                Full Name
              </span>
              <input
                className={getInputClass("name")}
                value={formData.name}
                onChange={(e) => {
                  setFormData({ ...formData, name: e.target.value });
                  if (errors.name) setErrors({ ...errors, name: "" });
                }}
                placeholder="e.g. Aman Gupta"
              />
              {errors.name && (
                <p className="text-red-500 text-[10px] font-bold mt-1">
                  {errors.name}
                </p>
              )}
            </label>

            {/* Position / Designation */}
            <label className="block">
              <span className="text-xs font-bold text-slate-500 uppercase mb-1.5 block">
                {positionLabel}
              </span>
              <input
                className={getInputClass("position")}
                value={formData.position}
                onChange={(e) => {
                  setFormData({ ...formData, position: e.target.value });
                  if (errors.position) setErrors({ ...errors, position: "" });
                }}
                placeholder={
                  isEmployee ? "Senior Software Engineer" : "Frontend Intern"
                }
              />
              {errors.position && (
                <p className="text-red-500 text-[10px] font-bold mt-1">
                  {errors.position}
                </p>
              )}
            </label>

            {/* Dates */}
            <label className="block">
              <span className="text-xs font-bold text-slate-500 uppercase mb-1.5 block">
                {dateLabel}
              </span>
              <input
                type="date"
                className={getInputClass("start_date")}
                value={formData.start_date}
                onChange={(e) =>
                  setFormData({ ...formData, start_date: e.target.value })
                }
              />
            </label>

            <label className="block">
              <span className="text-xs font-bold text-slate-500 uppercase mb-1.5 block">
                {isEmployee ? "Contract End (Optional)" : "End Date"}
              </span>
              <input
                type="date"
                className={getInputClass("end_date")}
                value={formData.end_date}
                onChange={(e) => {
                  setFormData({ ...formData, end_date: e.target.value });
                  if (errors.end_date) setErrors({ ...errors, end_date: "" });
                }}
              />
            </label>

            {/* Emails */}
            <label className="block">
              <span className="text-xs font-bold text-slate-500 uppercase mb-1.5 block">
                Work Email
              </span>
              <input
                className={getInputClass("contact_email")}
                value={formData.contact_email}
                onChange={(e) => {
                  setFormData({ ...formData, contact_email: e.target.value });
                  if (errors.contact_email)
                    setErrors({ ...errors, contact_email: "" });
                }}
                placeholder="name@leafclutch.com"
              />
              {errors.contact_email && (
                <p className="text-red-500 text-[10px] font-bold mt-1">
                  {errors.contact_email}
                </p>
              )}
            </label>

            <label className="block">
              <span className="text-xs font-bold text-slate-500 uppercase mb-1.5 block">
                Personal Email
              </span>
              <input
                className={getInputClass("personal_email")}
                value={formData.personal_email}
                onChange={(e) =>
                  setFormData({ ...formData, personal_email: e.target.value })
                }
                placeholder="personal.dev@gmail.com"
              />
            </label>

            {/* Contact & Visibility */}
            <label className="block">
              <span className="text-xs font-bold text-slate-500 uppercase mb-1.5 block">
                Contact Number
              </span>
              <input
                className={getInputClass("contact_number")}
                value={formData.contact_number}
                onChange={(e) =>
                  setFormData({ ...formData, contact_number: e.target.value })
                }
                placeholder="+91 XXXXX XXXXX"
              />
            </label>

            <div className="flex items-center justify-between p-3.5 bg-slate-50 rounded-2xl border border-slate-100 self-end">
              <span className="text-sm font-bold text-slate-700">
                Show on Website
              </span>
              <button
                type="button"
                onClick={() =>
                  setFormData({ ...formData, is_visible: !formData.is_visible })
                }
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  formData.is_visible ? "bg-accent-green" : "bg-slate-300"
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition duration-200 ${
                    formData.is_visible ? "translate-x-6" : "translate-x-1"
                  }`}
                />
              </button>
            </div>
          </div>

          {/* Social Media */}
          <div className="space-y-4 pt-4 border-t border-slate-100">
            <h3 className="text-sm font-extrabold text-primary-navy">
              Professional Profiles
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <label className="block">
                <span className="text-[10px] font-bold text-slate-400 uppercase mb-1 block">
                  LinkedIn
                </span>
                <input
                  className={getInputClass("linkedIn")}
                  value={formData.linkedIn}
                  onChange={(e) => {
                    setFormData({ ...formData, linkedIn: e.target.value });
                    if (errors.linkedIn) setErrors({ ...errors, linkedIn: "" });
                  }}
                  placeholder="https://linkedin.com/in/..."
                />
                {errors.linkedIn && (
                  <p className="text-red-500 text-[10px] mt-1">
                    {errors.linkedIn}
                  </p>
                )}
              </label>
              <label className="block">
                <span className="text-[10px] font-bold text-slate-400 uppercase mb-1 block">
                  Twitter
                </span>
                <input
                  className={getInputClass("twitter")}
                  value={formData.twitter}
                  onChange={(e) =>
                    setFormData({ ...formData, twitter: e.target.value })
                  }
                  placeholder="https://twitter.com/..."
                />
              </label>
              <label className="block">
                <span className="text-[10px] font-bold text-slate-400 uppercase mb-1 block">
                  GitHub
                </span>
                <input
                  className={getInputClass("github")}
                  value={formData.github}
                  onChange={(e) =>
                    setFormData({ ...formData, github: e.target.value })
                  }
                  placeholder="https://github.com/..."
                />
              </label>
            </div>
          </div>

          <div className="flex gap-4 pt-6">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-6 py-4 rounded-2xl border font-bold hover:bg-slate-50 transition-all"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-[2] px-6 py-4 rounded-2xl bg-accent-green text-primary-dark font-extrabold hover:shadow-lg transition-all active:scale-[0.98]"
            >
              {initialData ? `Update ${entityName}` : `Add ${entityName}`}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddUserModal;
