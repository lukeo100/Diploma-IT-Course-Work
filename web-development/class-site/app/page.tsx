"use client";

import { Class, getClasses } from "@/lib/api";
import { useState, useEffect } from "react";

export default function Home() {
  const [classes, setClasses] = useState<Class[] | undefined>();

  useEffect(() => {
    // avoid calling set state if component is unmounted
    let cancelled = false;

    // async function that fetches the data and updates state
    async function load() {
      const data = await getClasses();
      console.log(data);

      if (!cancelled) {
        setClasses(data);
      }
    }

    // start the fetch
    load();
    

    return () => {
      cancelled = true;
    };
  }, []);

  return <>

    {
      // This is the ternary operator again:
      //     condition ? valueIfTrue : valueIfFalse
      // `classes` is `undefined` (falsy) while loading, then becomes an array
      // (truthy) once loaded, so the correct branch is shown automatically.
      classes ?
        classes.map(c =>
          <div key={c.classID}>{c.subjectName}{c.teacherName}</div>
        )
        :
        <div key="loading">Loading..</div>
    }

  </>

};