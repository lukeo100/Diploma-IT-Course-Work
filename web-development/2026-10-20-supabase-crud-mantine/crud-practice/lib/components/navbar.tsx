"use client";
import { Anchor, Container, Group, Menu, Text } from '@mantine/core';

const navItems = [
	{ label: 'Home', href: '/' },
	{
		label: 'Mantine Tasks',
		href: '/mantine',
		items: [
			{ label: 'Products', href: '/mantine/' },
			{ label: 'Sign Up', href: '/mantine/sign-up' },
      { label: 'Feedback', href: '/mantine/feedback' },
		],
	},
	{ label: 'Supabase Practice', href: '/supabase' },
];

export default function Navbar() {
	return (
		<Container size="lg" py="md" id="tour-target-1">
			<Group justify="space-between">
				<Text component="a" href="/" fw={700} size="lg" c="inherit" td="none">
					CRUD Practice (with Mantine and Supabase)
				</Text>
				<Group gap="md">
					{navItems.map(({ label, href, items }) =>
						items ? (
							<Menu key={href} trigger="hover" openDelay={100} closeDelay={200}>
								<Menu.Target>
									<Anchor component="button" type="button" c="dimmed" underline="never">
										{label}
									</Anchor>
								</Menu.Target>
								<Menu.Dropdown>
									{items.map((item) => (
										<Menu.Item key={item.href} component="a" href={item.href}>
											{item.label}
										</Menu.Item>
									))}
								</Menu.Dropdown>
							</Menu>
						) : (
							<Anchor key={href} href={href} c="dimmed" underline="never">
								{label}
							</Anchor>
						),
					)}
				</Group>
			</Group>
		</Container>
	);
}
