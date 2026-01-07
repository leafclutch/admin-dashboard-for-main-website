import React from "react";

const BackgroundBlur: React.FC = () => {
  return (
    <div
      className="fixed inset-0 overflow-hidden pointer-events-none -z-10"
      aria-hidden="true"
    >
      <div className="absolute -top-[10%] -left-[10%] w-[40vw] h-[40vw] rounded-full bg-primary/10 blur-[100px]" />
      <div className="absolute -bottom-[15%] -right-[5%] w-[35vw] h-[35vw] rounded-full bg-primary/5 blur-[120px]" />
      <div className="absolute top-[20%] right-[10%] w-[20vw] h-[20vw] rounded-full bg-blue-400/5 blur-[80px]" />
    </div>
  );
};

export default BackgroundBlur;
