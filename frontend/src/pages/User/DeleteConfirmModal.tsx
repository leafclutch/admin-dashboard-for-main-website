import React from 'react';
import { Trash2, X } from 'lucide-react';

interface DeleteModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  itemName: string;
}

const DeleteConfirmModal: React.FC<DeleteModalProps> = ({ isOpen, onClose, onConfirm, itemName }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-[#102359]/20 backdrop-blur-md">
      <div className="bg-white rounded-[2rem] w-full max-w-sm p-8 shadow-2xl border border-slate-100 animate-in fade-in zoom-in duration-200">
        <div className="flex justify-end -mt-4 -mr-4">
          <button 
            onClick={onClose} 
            className="p-2 text-slate-400 hover:text-[#102359] transition-colors bg-slate-50 rounded-full"
          >
            <X size={18} />
          </button>
        </div>
        
        <div className="flex flex-col items-center text-center">
          <div className="w-20 h-20 bg-red-50 rounded-full flex items-center justify-center mb-6 border-4 border-white shadow-sm">
            <Trash2 className="text-red-500" size={32} />
          </div>
          
          <h2 className="text-2xl font-extrabold text-[#102359] tracking-tight mb-2">
            Are you sure?
          </h2>
          <p className="text-slate-500 text-sm font-medium leading-relaxed mb-8 px-4">
            You are about to delete <span className="text-[#102359] font-bold">"{itemName}"</span>. 
            This will remove them from the website. ok?
          </p>
          
          <div className="flex flex-col gap-3 w-full">
            <button 
              onClick={onConfirm}
              className="w-full py-4 bg-red-500 hover:bg-red-600 text-white font-bold rounded-2xl shadow-lg shadow-red-100 transition-all active:scale-95"
            >
              Yes, Delete Permanent
            </button>
            <button 
              onClick={onClose}
              className="w-full py-4 bg-white border border-slate-200 text-slate-600 font-bold rounded-2xl hover:bg-slate-50 transition-all"
            >
              No, Keep it
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmModal;