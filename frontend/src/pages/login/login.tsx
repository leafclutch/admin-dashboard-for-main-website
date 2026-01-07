import React from "react";
import LoginForm from "./LoginForm";
import BackgroundBlur from "./BackgroundBlur";

const App: React.FC = () => {
  return (
    <main className="relative min-h-screen w-full flex flex-col items-center justify-center p-4 selection:bg-accent-teal/20 selection:text-primary-dark bg-background-base">
      <BackgroundBlur />

      <div className="relative z-10 w-full max-w-[460px] animate-in fade-in zoom-in duration-700">
        <LoginForm />

        <footer className="mt-8 text-center">
          <p className="text-xs text-slate-400 font-medium tracking-wide">
            &copy; {new Date().getFullYear()} Leafclutch Technologies. All
            rights reserved.
          </p>
        </footer>
      </div>
    </main>
  );
};

export default App;
