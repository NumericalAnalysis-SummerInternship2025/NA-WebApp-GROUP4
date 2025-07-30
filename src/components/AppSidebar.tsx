import { Calculator, Home, BookOpen, Search, MessageCircle, ArrowLeft, Users, LogOut, User } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { UserProfileDialog } from "@/components/UserProfileDialog";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  SidebarFooter,
  SidebarInput,
} from "@/components/ui/sidebar";

const navigationItems = [
  {
    title: "Accueil",
    url: "/",
    icon: Home,
  },
  {
    title: "À propos",
    url: "/about",
    icon: Users,
  },
  {
    title: "Tableau de Bord",
    url: "/professor-dashboard",
    icon: BookOpen,
    adminOnly: true
  },
  {
    title: "Modules",
    url: "/modules",
    icon: BookOpen,
  },
  {
    title: "Outils Interactifs",
    url: "/tools",
    icon: Calculator,
  },
  {
    title: "Mode Exam",
    url: "/mode-exam",
    icon: Calculator,
  },
];

const modules = [
  {
    title: "Systèmes linéaires",
    url: "/module/systemes-lineaires",
    icon: Calculator,
  },
  {
    title: "Interpolation",
    url: "/module/interpolation",
    icon: Calculator,
  },
  {
    title: "Intégration numérique",
    url: "/module/integration",
    icon: Calculator,
  },
  {
    title: "Équations non linéaires",
    url: "/module/equations-non-lineaires",
    icon: Calculator,
  },
];

export function AppSidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <Sidebar className="border-r bg-white">
      <SidebarHeader className="p-4">
        <div className="flex items-center space-x-2">
          <Calculator className="h-8 w-8 text-blue-600" />
          <h1 className="text-xl font-bold text-gray-900">NumiViz</h1>
        </div>
        <div className="mt-4">
          <SidebarInput 
            placeholder="Rechercher un module..." 
            className="bg-gray-50"
          />
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navigationItems.map((item) => {
                // Ne pas afficher les éléments adminOnly si l'utilisateur n'est pas professeur
                if (item.adminOnly && (!user || user.role !== 'professeur')) {
                  return null;
                }
                
                return (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton 
                      asChild
                      isActive={location.pathname === item.url}
                    >
                      <button 
                        onClick={() => navigate(item.url)}
                        className="w-full"
                      >
                        <item.icon className="h-4 w-4" />
                        <span>{item.title}</span>
                      </button>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Modules Disponibles</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {modules.map((module) => (
                <SidebarMenuItem key={module.title}>
                  <SidebarMenuButton 
                    asChild
                    isActive={location.pathname === module.url}
                  >
                    <button 
                      onClick={() => navigate(module.url)}
                      className="w-full"
                    >
                      <module.icon />
                      <span className="text-sm">{module.title}</span>
                    </button>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="p-4">
        <SidebarMenu>
          {isAuthenticated && user && (
            <SidebarMenuItem>
              <UserProfileDialog />
            </SidebarMenuItem>
          )}
          <SidebarMenuItem>
            <SidebarMenuButton asChild>
              <button className="w-full flex items-center gap-2 text-gray-600 hover:text-blue-600">
                <MessageCircle />
                <span>Questions & Aide</span>
              </button>
            </SidebarMenuButton>
          </SidebarMenuItem>
          {isAuthenticated && (
            <SidebarMenuItem>
              <SidebarMenuButton asChild>
                <button 
                  onClick={() => {
                    logout();
                    navigate('/');
                  }}
                  className="w-full flex items-center gap-2 text-red-600 hover:text-red-700"
                >
                  <LogOut />
                  <span>Déconnexion</span>
                </button>
              </SidebarMenuButton>
            </SidebarMenuItem>
          )}
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
