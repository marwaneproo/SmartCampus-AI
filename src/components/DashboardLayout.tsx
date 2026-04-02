import { useAuth } from "@/contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { LogOut, GraduationCap } from "lucide-react";
import { ReactNode } from "react";

interface DashboardLayoutProps {
  title: string;
  children: ReactNode;
}

const DashboardLayout = ({ title, children }: DashboardLayoutProps) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-primary shadow-md">
        <div className="container mx-auto flex items-center justify-between px-4 py-3">
          <div className="flex items-center gap-3">
            <GraduationCap className="h-8 w-8 text-primary-foreground" />
            <div>
              <h1 className="text-lg font-heading font-bold text-primary-foreground">
                EMSI ClassFlow
              </h1>
              <p className="text-xs text-primary-foreground/80">{title}</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <span className="hidden sm:inline text-sm text-primary-foreground/90">
              ID: {user?.userId} • {user?.role}
            </span>
            <Button variant="secondary" size="sm" onClick={handleLogout}>
              <LogOut className="h-4 w-4 mr-1" /> Logout
            </Button>
          </div>
        </div>
      </header>
      <main className="container mx-auto px-4 py-6 animate-fade-in">
        {children}
      </main>
    </div>
  );
};

export default DashboardLayout;
