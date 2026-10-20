import "@mantine/core/styles.css";
import '@mantine/tiptap/styles.css';
import { MantineProvider } from "@mantine/core";
import Navbar from "@/lib/components/navbar";

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body>
                <MantineProvider>
                    <Navbar />
                    {children}
                </MantineProvider>
            </body>
        </html>
    );
}