export interface SocialMedia {
  linkedIn?: string;
  twitter?: string;
  github?: string;
}

export interface User {
  id: string;
  photo_url: string;
  name: string;
  position: string;
  start_date: string;
  end_date: string | null;
  social_media: SocialMedia;
  contact_email: string;
  personal_email: string;
  contact_number: string;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface StatData {
  label: string;
  value: string | number;
  icon: React.ReactNode;
  trend?: {
    type: "success" | "warning" | "neutral";
    icon?: React.ReactNode;
    text: string;
  };
}
