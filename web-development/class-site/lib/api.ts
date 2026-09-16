const NEXT_PUBLIC_SUPABASE_URL: string = 'https://cbdnpfmerhbbxgqjqvig.supabase.co/rest/v1/';
const NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY: string = 'sb_publishable_2Wd0HbjkZROjq_PLAQ3iqA_QHnitTWk';

export interface Class {
    classID: string;
    teacherID: string;
    teacherName: string;
    subjectCode: string;
    subjectName: string;
    room?: string;
    day?: string;
    startTime?: Date;
    endTime?: Date;
    createdAt?: Date;
}

export async function getClasses(): Promise<Class[]> {
    // 1. Start the network request wait for it to finish
    const response = await fetch(`${NEXT_PUBLIC_SUPABASE_URL}/class`, {
        headers: {
            "apikey": NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY,
        },
    });

    // 2. convert to json
    const data = (await response.json()) as Class[];

    // 3. Return the data. Because this is an async function, returning a value automatically wraps it in a resolved Promise for the caller.
    return data;
}