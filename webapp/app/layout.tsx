import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://signaldesk-weekly-health.dngrdoom.chatgpt.site"),
  title: "SignalDesk Weekly Health",
  description: "A decision-focused weekly health check for AI-assisted workflows.",
  openGraph: {
    title: "SignalDesk AI Workflow Health Dashboard",
    description: "A decision-focused weekly health check for AI-assisted workflows.",
    images: ["/og-v3.png"],
  },
  twitter: {
    card: "summary_large_image",
    title: "SignalDesk AI Workflow Health Dashboard",
    description: "A decision-focused weekly health check for AI-assisted workflows.",
    images: ["/og-v3.png"],
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
