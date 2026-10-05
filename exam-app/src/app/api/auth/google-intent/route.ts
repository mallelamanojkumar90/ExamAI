import { NextResponse } from "next/server";

const VALID_INTENTS = new Set(["login", "signup"]);

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const intent = typeof body.intent === "string" ? body.intent : "";

  if (!VALID_INTENTS.has(intent)) {
    return NextResponse.json({ error: "Invalid Google auth intent" }, { status: 400 });
  }

  const response = NextResponse.json({ ok: true });
  response.cookies.set("google_auth_intent", intent, {
    httpOnly: true,
    maxAge: 5 * 60,
    path: "/",
    sameSite: "lax",
  });

  return response;
}
