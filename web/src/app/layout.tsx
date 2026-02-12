import './globals.css';
import { ReactNode } from 'react';
import EjadaLogo from '../components/EjadaLogo';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900">
        <header className="bg-white border-b flex items-center p-3">
          <EjadaLogo />
          <h1 className="ml-3 font-semibold">Ejada Leave Portal</h1>
        </header>
        <main className="max-w-6xl mx-auto p-6">{children}</main>
      </body>
    </html>
  );
}