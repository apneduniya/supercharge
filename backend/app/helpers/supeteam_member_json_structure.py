import typing as t


def generate_member_content(member: t.Dict[str, t.Any]) -> str:
    """Format the member data into a comprehensive content string."""
    formatted_member = [
        f"Name: {member['name']}",
        f"Username: {member['username']}",
        f"Bio: {member['profile'].get('bio', '')}",
        f"Work: {member['profile'].get('work', 'N/A')}",
        f"Location: {member['profile'].get('location', 'N/A')}",
        f"Skills: {' '.join([', '.join(skills) for skills in member['profile']['skills'].values() if skills])}",
    ]

    # Create a comprehensive content string
    content = " ".join(filter(None, formatted_member))

    return content


def generate_member_metadata(member: t.Dict[str, t.Any]) -> t.List[t.Dict[str, t.Any]]:
    """Generate metadata from the member data."""
    metadata = {
        "id": member['id'],
        "name": member['name'],
        "username": member['username'],
        "work": member['profile'].get('work'),
        "location": member['profile'].get('location'),
        "skills": member['profile']['skills'],
        "earnings": member['profile']['earnings'],
        "submissions": member['profile']['submissions'],
        "wins": member['profile']['wins']
    }

    return metadata
