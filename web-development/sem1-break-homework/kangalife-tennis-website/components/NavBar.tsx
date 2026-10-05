import Link from "next/link";

// No hooks here, so this can stay a Server Component (no "use client" needed).
export default function NavBar() {
  return (
    <nav>
      <Link href="/">Home</Link>
      {" | "}
      <Link href="/courts">Courts</Link>
      {" | "}
      <Link href="/members">Members</Link>
      <hr />
    </nav>
  );
}
