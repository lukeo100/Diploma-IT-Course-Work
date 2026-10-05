"use client";
import type { Member } from "@/lib/types";
import { useState, useEffect } from "react";
import { getMembers } from "@/lib/api";
import Link from "next/link";

// MEMBERS LIST: every member, each linking to their own page at /members/[member_id].

export default function MembersPage() {
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let isCancelled = false

    async function loadData() {
      setLoading(true)
      setError(null)
      try {
        const result = await getMembers()
        if (!isCancelled) {
          setMembers(result)
        }
      } catch (err: unknown) {
        if (!isCancelled) {
          setError(err instanceof Error ? err.message : 'Something went wrong')
        }
      } finally {
        if (!isCancelled) {
          setLoading(false)
        }
      }
    }

    loadData()

    // Cleanup function prevents setting state on unmounted component
    return () => {
      isCancelled = true
    }
  }, [])

  if (loading) return <p>Loading...</p>
  if (error) return <p>Error: {error}</p>
  if (!members.length) return <p>No data found.</p>

  return (
    <main>
      <h1>Members</h1>
      <ul>
        {members.map((member) => (
          <li key={member.member_id}>
            <Link href={`/members/${member.member_id}`}>
              {member.name} | {member.member_level}
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
