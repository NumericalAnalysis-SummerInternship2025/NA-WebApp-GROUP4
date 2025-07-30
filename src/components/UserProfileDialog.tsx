import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";
import { User } from "lucide-react";

export function UserProfileDialog() {
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <Dialog>
      <DialogTrigger asChild>
        <button className="w-full flex items-center gap-2 text-gray-600 hover:text-blue-600">
          <User className="w-4 h-4" />
          <span>{user.name}</span>
        </button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Mon Profil</DialogTitle>
        </DialogHeader>
        <div className="space-y-2 py-2">
          <div><b>Nom :</b> {user.name}</div>
          <div><b>Email :</b> {user.email}</div>
          <div><b>Rôle :</b> {user.role}</div>
        </div>
        <Button variant="destructive" onClick={logout}>Déconnexion</Button>
      </DialogContent>
    </Dialog>
  );
} 