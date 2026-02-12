"use client";
import { useEffect, useState } from 'react';
import api, { setToken } from '../lib/api';

export default function Dashboard() {
  const [token, setTok] = useState<string | null>(null);
  const [requests, setRequests] = useState<any[]>([]);

  useEffect(() => {
    const t = localStorage.getItem('token');
    if (t) { setTok(t); setToken(t); }
  }, []);

  useEffect(() => {
    if (!token) return;
    api.get('/leave-requests').then(res => setRequests(res.data));
  }, [token]);

  return (
    <div>
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">My Leave Requests</h2>
        <a href="/requests/new" className="px-4 py-2 bg-indigo-600 text-white rounded">New Request</a>
      </div>
      <div className="mt-4 bg-white rounded shadow">
        <table className="w-full">
          <thead>
            <tr className="text-left border-b">
              <th className="p-3">ID</th>
              <th className="p-3">Type</th>
              <th className="p-3">Dates</th>
              <th className="p-3">Days</th>
              <th className="p-3">Status</th>
            </tr>
          </thead>
          <tbody>
            {requests.map((r) => (
              <tr key={r.id} className="border-b">
                <td className="p-3">{r.id}</td>
                <td className="p-3">{r.leave_type_id}</td>
                <td className="p-3">{r.start_date} → {r.end_date}</td>
                <td className="p-3">{r.days}</td>
                <td className="p-3">{r.status}</td>
              </tr>
            ))}
            {requests.length === 0 && <tr><td className="p-3">No requests yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}