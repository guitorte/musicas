#!/usr/bin/env python3
"""
Syntax and Pronoun Analysis for Portuguese Lyrics
Analyzes explicit vs implicit "eu" usage in verb conjugation
"""

import json
import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple

class SyntaxAnalyzer:
    """Analyzes Portuguese syntax patterns in lyrics"""

    def __init__(self, json_file: str):
        with open(json_file, 'r', encoding='utf-8') as f:
            self.songs = json.load(f)

        # Common first-person verb endings in Portuguese
        self.first_person_patterns = [
            # Present tense
            r'\b(\w+)(o|ei|ou|ava|ia|arei|erei|irei|aria|eria|iria|asse|esse|isse|ar|er|ir)\b',
        ]

        # More specific patterns for common verbs
        self.specific_verbs = {
            # Present indicative
            'present': [
                r'\bsou\b', r'\bestou\b', r'\btenho\b', r'\bfaço\b', r'\bvou\b',
                r'\bquero\b', r'\bamo\b', r'\bsinto\b', r'\bsei\b', r'\bposso\b',
                r'\bvejo\b', r'\bdigo\b', r'\bfico\b', r'\bdou\b', r'\bpasso\b',
                r'\bvivo\b', r'\bsinto\b', r'\bponho\b', r'\bvenho\b', r'\bsaio\b',
                r'\bpeço\b', r'\btrago\b', r'\bconheço\b', r'\bperco\b'
            ],
            # Past (preterite)
            'preterite': [
                r'\bfui\b', r'\bestive\b', r'\btive\b', r'\bfiz\b', r'\bquis\b',
                r'\bamei\b', r'\bsenti\b', r'\bsoube\b', r'\bpude\b', r'\bvi\b',
                r'\bdisse\b', r'\bfiquei\b', r'\bdei\b', r'\bpassei\b', r'\bvivi\b'
            ],
            # Imperfect
            'imperfect': [
                r'\bera\b', r'\bestava\b', r'\btinha\b', r'\bfazia\b', r'\bia\b',
                r'\bqueria\b', r'\bamava\b', r'\bsentia\b', r'\bsabia\b', r'\bpodia\b'
            ],
            # Future
            'future': [
                r'\bserei\b', r'\bestarei\b', r'\bterei\b', r'\bfarei\b', r'\birei\b',
                r'\bquerei\b', r'\bamarei\b', r'\bverei\b'
            ],
            # Conditional
            'conditional': [
                r'\bseria\b', r'\bestaria\b', r'\bteria\b', r'\bfaria\b', r'\biria\b',
                r'\bquereria\b', r'\bamaria\b', r'\bveria\b'
            ]
        }

    def analyze_pronoun_usage(self) -> Dict:
        """Analyze explicit vs implicit 'eu' usage"""

        print("🔍 Analyzing pronoun usage patterns...")

        stats = {
            'total_lines': 0,
            'explicit_eu': 0,
            'implicit_eu': 0,
            'explicit_examples': [],
            'implicit_examples': [],
            'verb_tense_distribution': defaultdict(lambda: {'explicit': 0, 'implicit': 0}),
            'position_analysis': {'eu_verb': 0, 'verb_eu': 0},  # word order
            'other_pronouns': Counter()
        }

        # Compile all verb patterns
        all_verbs = []
        for tense, patterns in self.specific_verbs.items():
            for pattern in patterns:
                all_verbs.append((tense, re.compile(pattern, re.IGNORECASE)))

        # Analyze each song
        for song in self.songs[:]:  # Analyze all songs
            letra = song.get('letra', '')
            lines = letra.split('\n')

            for line in lines:
                line = line.strip()
                if len(line) < 3:
                    continue

                stats['total_lines'] += 1

                # Check for explicit "eu"
                has_explicit_eu = bool(re.search(r'\beu\b', line, re.IGNORECASE))

                # Check for first-person verbs
                found_verb = False
                verb_tense = None

                for tense, verb_pattern in all_verbs:
                    if verb_pattern.search(line):
                        found_verb = True
                        verb_tense = tense
                        break

                if found_verb:
                    if has_explicit_eu:
                        stats['explicit_eu'] += 1
                        stats['verb_tense_distribution'][verb_tense]['explicit'] += 1

                        # Check word order (eu verb vs verb eu)
                        if re.search(r'\beu\s+\w+', line, re.IGNORECASE):
                            stats['position_analysis']['eu_verb'] += 1
                        elif re.search(r'\w+\s+eu\b', line, re.IGNORECASE):
                            stats['position_analysis']['verb_eu'] += 1

                        # Collect examples
                        if len(stats['explicit_examples']) < 50:
                            stats['explicit_examples'].append(line)
                    else:
                        stats['implicit_eu'] += 1
                        stats['verb_tense_distribution'][verb_tense]['implicit'] += 1

                        # Collect examples
                        if len(stats['implicit_examples']) < 50:
                            stats['implicit_examples'].append(line)

                # Count other pronouns
                for pronoun in ['você', 'tu', 'ele', 'ela', 'nós', 'vocês', 'eles', 'elas']:
                    if re.search(r'\b' + pronoun + r'\b', line, re.IGNORECASE):
                        stats['other_pronouns'][pronoun] += 1

        return stats

    def analyze_sentence_structure(self) -> Dict:
        """Analyze typical sentence structures"""

        print("📊 Analyzing sentence structures...")

        structures = {
            'svo': 0,  # Subject-Verb-Object
            'vso': 0,  # Verb-Subject-Object (inverted)
            'vo': 0,   # Verb-Object (null subject)
            'sv': 0,   # Subject-Verb
            'v': 0,    # Verb only
            'examples': defaultdict(list)
        }

        sample_count = 0
        max_samples = 1000

        for song in self.songs:
            letra = song.get('letra', '')
            lines = letra.split('\n')

            for line in lines:
                line = line.strip()
                if len(line) < 5 or sample_count >= max_samples:
                    continue

                # Simple heuristics for sentence structure
                words = line.split()

                # Check for explicit subject at start
                starts_with_pronoun = bool(re.match(r'^(eu|você|tu|ele|ela|nós)\b', line, re.IGNORECASE))

                # Check for verb
                has_first_person_verb = False
                for tense, patterns in self.specific_verbs.items():
                    for pattern in patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            has_first_person_verb = True
                            break
                    if has_first_person_verb:
                        break

                if has_first_person_verb:
                    if starts_with_pronoun:
                        if re.search(r'\beu\b', line, re.IGNORECASE):
                            structures['svo'] += 1
                            if len(structures['examples']['svo']) < 10:
                                structures['examples']['svo'].append(line)
                    else:
                        # Verb without explicit subject (null subject)
                        structures['vo'] += 1
                        if len(structures['examples']['vo']) < 10:
                            structures['examples']['vo'].append(line)

                    sample_count += 1

        return structures

    def print_report(self, pronoun_stats: Dict, structure_stats: Dict):
        """Print comprehensive analysis report"""

        print("\n" + "=" * 80)
        print("🎵 PORTUGUESE SYNTAX ANALYSIS - LYRICS COLLECTION")
        print("=" * 80)

        # Pronoun usage summary
        total_first_person = pronoun_stats['explicit_eu'] + pronoun_stats['implicit_eu']
        explicit_pct = (pronoun_stats['explicit_eu'] / total_first_person * 100) if total_first_person > 0 else 0
        implicit_pct = (pronoun_stats['implicit_eu'] / total_first_person * 100) if total_first_person > 0 else 0

        print("\n📊 PRONOUN USAGE SUMMARY")
        print("-" * 80)
        print(f"Total lines analyzed: {pronoun_stats['total_lines']:,}")
        print(f"Total first-person constructions: {total_first_person:,}")
        print()
        print(f"✓ EXPLICIT 'eu': {pronoun_stats['explicit_eu']:,} ({explicit_pct:.1f}%)")
        print(f"✓ IMPLICIT (null subject): {pronoun_stats['implicit_eu']:,} ({implicit_pct:.1f}%)")
        print()

        # Key finding
        if implicit_pct > explicit_pct:
            ratio = implicit_pct / explicit_pct if explicit_pct > 0 else 0
            print(f"🔍 KEY FINDING: Portuguese lyrics use IMPLICIT subject {ratio:.1f}x more than explicit 'eu'")
        else:
            ratio = explicit_pct / implicit_pct if implicit_pct > 0 else 0
            print(f"🔍 KEY FINDING: Portuguese lyrics use EXPLICIT 'eu' {ratio:.1f}x more than implicit")

        # Verb tense distribution
        print("\n📈 VERB TENSE DISTRIBUTION")
        print("-" * 80)
        for tense in sorted(pronoun_stats['verb_tense_distribution'].keys()):
            data = pronoun_stats['verb_tense_distribution'][tense]
            total = data['explicit'] + data['implicit']
            exp_pct = (data['explicit'] / total * 100) if total > 0 else 0
            imp_pct = (data['implicit'] / total * 100) if total > 0 else 0

            print(f"\n{tense.upper()}:")
            print(f"  Total: {total:,}")
            print(f"  └─ Explicit 'eu': {data['explicit']:,} ({exp_pct:.1f}%)")
            print(f"  └─ Implicit: {data['implicit']:,} ({imp_pct:.1f}%)")

        # Word order analysis
        print("\n📍 WORD ORDER (when 'eu' is explicit)")
        print("-" * 80)
        total_ordered = pronoun_stats['position_analysis']['eu_verb'] + pronoun_stats['position_analysis']['verb_eu']
        if total_ordered > 0:
            ev_pct = pronoun_stats['position_analysis']['eu_verb'] / total_ordered * 100
            ve_pct = pronoun_stats['position_analysis']['verb_eu'] / total_ordered * 100
            print(f"'eu' + verb: {pronoun_stats['position_analysis']['eu_verb']:,} ({ev_pct:.1f}%)")
            print(f"verb + 'eu': {pronoun_stats['position_analysis']['verb_eu']:,} ({ve_pct:.1f}%)")
            print(f"\n→ Standard SVO order is {'dominant' if ev_pct > ve_pct else 'not dominant'}")

        # Other pronouns
        print("\n👥 OTHER PRONOUN USAGE (for comparison)")
        print("-" * 80)
        for pronoun, count in pronoun_stats['other_pronouns'].most_common(10):
            print(f"{pronoun}: {count:,}")

        # Examples
        print("\n📝 EXAMPLES OF EXPLICIT 'EU'")
        print("-" * 80)
        for i, example in enumerate(pronoun_stats['explicit_examples'][:15], 1):
            print(f"{i}. {example}")

        print("\n📝 EXAMPLES OF IMPLICIT (NULL SUBJECT)")
        print("-" * 80)
        for i, example in enumerate(pronoun_stats['implicit_examples'][:15], 1):
            print(f"{i}. {example}")

        # Sentence structure summary
        print("\n🏗️  SENTENCE STRUCTURE PATTERNS")
        print("-" * 80)
        total_structures = sum([structure_stats['svo'], structure_stats['vo']])
        if total_structures > 0:
            svo_pct = structure_stats['svo'] / total_structures * 100
            vo_pct = structure_stats['vo'] / total_structures * 100

            print(f"Subject + Verb + (Object): {structure_stats['svo']:,} ({svo_pct:.1f}%)")
            print(f"Verb + (Object) - null subject: {structure_stats['vo']:,} ({vo_pct:.1f}%)")

        print("\n" + "=" * 80)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 80)


def main():
    """Main execution"""

    print("=" * 80)
    print("🎵 PORTUGUESE SYNTAX ANALYZER")
    print("=" * 80)

    analyzer = SyntaxAnalyzer('/home/user/musicas/all_lyrics.json')

    # Run analyses
    pronoun_stats = analyzer.analyze_pronoun_usage()
    structure_stats = analyzer.analyze_sentence_structure()

    # Print report
    analyzer.print_report(pronoun_stats, structure_stats)

    # Save detailed results
    results = {
        'pronoun_analysis': {
            'total_lines': pronoun_stats['total_lines'],
            'explicit_eu': pronoun_stats['explicit_eu'],
            'implicit_eu': pronoun_stats['implicit_eu'],
            'explicit_percentage': (pronoun_stats['explicit_eu'] / (pronoun_stats['explicit_eu'] + pronoun_stats['implicit_eu']) * 100) if (pronoun_stats['explicit_eu'] + pronoun_stats['implicit_eu']) > 0 else 0,
            'implicit_percentage': (pronoun_stats['implicit_eu'] / (pronoun_stats['explicit_eu'] + pronoun_stats['implicit_eu']) * 100) if (pronoun_stats['explicit_eu'] + pronoun_stats['implicit_eu']) > 0 else 0,
            'verb_tense_distribution': dict(pronoun_stats['verb_tense_distribution']),
            'word_order': pronoun_stats['position_analysis'],
            'other_pronouns': dict(pronoun_stats['other_pronouns'])
        },
        'structure_analysis': {
            'svo': structure_stats['svo'],
            'vo': structure_stats['vo']
        }
    }

    with open('/home/user/musicas/syntax_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n💾 Detailed results saved to: syntax_analysis.json")


if __name__ == "__main__":
    main()
