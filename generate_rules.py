#!/usr/bin/env python3
"""보드게임 룰마스터 에이전트 — 게임 이름을 입력하면 룰 파일을 생성합니다."""

import sys
import anthropic
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("사용법: python generate_rules.py <게임이름>")
        print("예시:   python generate_rules.py 푸에르토리코")
        sys.exit(1)

    game_name = " ".join(sys.argv[1:])
    output_file = Path(__file__).parent / f"{game_name}.md"

    system_prompt = (Path(__file__).parent / "Agent.md").read_text(encoding="utf-8")

    client = anthropic.Anthropic()

    print(f"'{game_name}' 룰을 생성 중...\n")
    print("-" * 60)

    content = ""
    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=8000,
        system=system_prompt,
        messages=[{"role": "user", "content": game_name}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            content += text

    print("\n" + "-" * 60)
    output_file.write_text(content, encoding="utf-8")
    print(f"\n저장 완료: {output_file.name}")


if __name__ == "__main__":
    main()
