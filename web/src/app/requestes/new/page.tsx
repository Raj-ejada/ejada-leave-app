"use client";
import { useState } from 'react';
import api from '../../../lib/api';
import { useRouter } from 'next/navigation';

export default function NewRequest() {
  const [leaveTypeId, setLeaveTypeId] = useState(1);
  const [reason, setReason] = useState('');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [isHalf, setIsHalf] = useState(false);
  const [msg, setMsg] = useState('');
  const router = useRouter();

  const create = async () => {
    try {
      const res = await api.post('/leave-requests', {
        leave_type_id: leaveTypeId,
        reason,
        start_date: start,
        end_date: end,
        is_half_day: isHalf
      });
      await api.patch(`/leave-requests/${res.data.id}/submit`);
      setMsg('Submitted successfully');
      setTimeout(() => router.push('/'), 1000);
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || 'Error');
    }
  };

  return (
    <div className="max-w-xl bg-white p-6 rounded shadow">
      <h2 className="text-lg font-bold mb-4">New Leave Request</h2>
      {msg && <div className="mb-2">{msg}</div>}
      <label className="block mb-2">Leave Type</label>
      <select value={leaveTypeId} onChange={e=>setLeaveTypeId(Number(e.target.value))} className="border p-2 w-full mb-3">
        <option value={1}>Casual Leave</option>
        <option value={2}>Earned Leave</option>
        <option value={3}>Sick Leave</option>
        <option value={4}>Unpaid</option>
      </select>
      <label className="block mb-2">From</label>
      <input type="date" value={start} onChange={e=>setStart(e.target.value)} className="border p-2 w-full mb-3" />
      <label className="block mb-2">To</label>
      <input type="date" value={end} onChange={e=>setEnd(e.target.value)} className="border p-2 w-full mb-3" />
      <label className="flex items-center gap-2 mb-3">
        <input type="checkbox" checked={isHalf} onChange={e=>setIsHalf(e.target.checked)} />
        Half day
      </label>
      <label className="block mb-2">Reason (optional)</label>
      <textarea value={reason} onChange={e=>setReason(e.target.value)} className="border p-2 w-full mb-3" />
      <button onClick={create} className="bg-indigo-600 text-white px-4 py-2 rounded">Submit</button>
    </div>
  );
}
