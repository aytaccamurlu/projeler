import { NextResponse } from 'next/server';

export async function GET() {
  const BACKEND_URL = "http://127.0.0.1:5000/customers";
  
  try {
    const res = await fetch(BACKEND_URL, {
      cache: 'no-store',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: 'Backend erişim hatası' }, { status: 500 });
  }
}