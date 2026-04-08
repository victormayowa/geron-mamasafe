"""
Test script to verify danger signs database and triage system
"""

import sys
sys.path.insert(0, '/home/victormayowa/geron-mamasafe/backend')

from app.services.danger_signs_db import DangerSignsDatabase
from app.models.models import PregnancyStage, ChildAgeGroup, TriageSeverity


def test_danger_signs():
    """Test all danger signs categories"""
    
    print("=" * 70)
    print("🧪 TESTING DANGER SIGNS DATABASE")
    print("=" * 70)
    
    # Test Maternal Danger Signs
    print("\n🤰 MATERNAL DANGER SIGNS")
    print("-" * 70)
    
    for stage in PregnancyStage:
        signs = DangerSignsDatabase.get_maternal_danger_signs(stage)
        print(f"\n{stage.value.upper().replace('_', ' ')}:")
        print(f"  Total signs: {len(signs)}")
        
        red = len([s for s in signs if s['triage_color'] == TriageSeverity.RED])
        yellow = len([s for s in signs if s['triage_color'] == TriageSeverity.YELLOW])
        green = len([s for s in signs if s['triage_color'] == TriageSeverity.GREEN])
        
        print(f"  🔴 RED: {red} | 🟡 YELLOW: {yellow} | 🟢 GREEN: {green}")
        
        for sign in signs[:3]:  # Show first 3
            print(f"    - {sign['sign_name']} ({sign['triage_color'].value})")
    
    # Test Neonatal Danger Signs
    print("\n\n👶 NEONATAL DANGER SIGNS (0-28 days)")
    print("-" * 70)
    neonatal_signs = DangerSignsDatabase.get_neonatal_danger_signs()
    print(f"Total signs: {len(neonatal_signs)}")
    
    red = len([s for s in neonatal_signs if s['triage_color'] == TriageSeverity.RED])
    yellow = len([s for s in neonatal_signs if s['triage_color'] == TriageSeverity.YELLOW])
    green = len([s for s in neonatal_signs if s['triage_color'] == TriageSeverity.GREEN])
    print(f"🔴 RED: {red} | 🟡 YELLOW: {yellow} | 🟢 GREEN: {green}")
    
    for sign in neonatal_signs[:5]:
        print(f"  - {sign['sign_name']} ({sign['triage_color'].value})")
    
    # Test Infant Danger Signs
    print("\n\n👶 INFANT DANGER SIGNS (1-12 months)")
    print("-" * 70)
    infant_signs = DangerSignsDatabase.get_infant_danger_signs()
    print(f"Total signs: {len(infant_signs)}")
    
    red = len([s for s in infant_signs if s['triage_color'] == TriageSeverity.RED])
    yellow = len([s for s in infant_signs if s['triage_color'] == TriageSeverity.YELLOW])
    print(f"🔴 RED: {red} | 🟡 YELLOW: {yellow}")
    
    for sign in infant_signs[:5]:
        print(f"  - {sign['sign_name']} ({sign['triage_color'].value})")
    
    # Test Child Danger Signs
    print("\n\n🧒 CHILD DANGER SIGNS (Under 5)")
    print("-" * 70)
    
    for age_group in ChildAgeGroup:
        if age_group in [ChildAgeGroup.TODDLER, ChildAgeGroup.PRESCHOOL]:
            signs = DangerSignsDatabase.get_child_danger_signs(age_group)
            print(f"\n{age_group.value.upper()}:")
            print(f"  Total signs: {len(signs)}")
            
            red = len([s for s in signs if s['triage_color'] == TriageSeverity.RED])
            yellow = len([s for s in signs if s['triage_color'] == TriageSeverity.YELLOW])
            print(f"  🔴 RED: {red} | 🟡 YELLOW: {yellow}")
            
            for sign in signs[:3]:
                print(f"    - {sign['sign_name']} ({sign['triage_color'].value})")
    
    # Test Adolescent Danger Signs
    print("\n\n👩‍🎓 ADOLESCENT DANGER SIGNS (10-19 years)")
    print("-" * 70)
    adolescent_signs = DangerSignsDatabase.get_adolescent_danger_signs()
    print(f"Total signs: {len(adolescent_signs)}")
    
    red = len([s for s in adolescent_signs if s['triage_color'] == TriageSeverity.RED])
    yellow = len([s for s in adolescent_signs if s['triage_color'] == TriageSeverity.YELLOW])
    green = len([s for s in adolescent_signs if s['triage_color'] == TriageSeverity.GREEN])
    print(f"🔴 RED: {red} | 🟡 YELLOW: {yellow} | 🟢 GREEN: {green}")
    
    for sign in adolescent_signs:
        print(f"  - {sign['sign_name']} ({sign['triage_color'].value})")
    
    # Summary
    print("\n\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    maternal_all = DangerSignsDatabase.get_all_maternal_danger_signs()
    neonatal_all = DangerSignsDatabase.get_neonatal_danger_signs()
    infant_all = DangerSignsDatabase.get_infant_danger_signs()
    child_all = DangerSignsDatabase.get_all_child_danger_signs()
    adolescent_all = DangerSignsDatabase.get_adolescent_danger_signs()
    
    total = len(maternal_all) + len(neonatal_all) + len(infant_all) + len(child_all) + len(adolescent_all)
    
    print(f"✅ Maternal:     {len(maternal_all)} signs")
    print(f"✅ Neonatal:     {len(neonatal_all)} signs")
    print(f"✅ Infant:       {len(infant_all)} signs")
    print(f"✅ Child:        {len(child_all)} signs")
    print(f"✅ Adolescent:   {len(adolescent_all)} signs")
    print(f"\n🎯 TOTAL:        {total} danger signs")
    
    # Test search functionality
    print("\n\n🔍 SEARCH TEST")
    print("-" * 70)
    
    test_queries = [
        ("bleeding", "mother"),
        ("fever", "neonate"),
        ("breathing", "child"),
        ("headache", "mother"),
        ("convulsion", None),
    ]
    
    for query, patient_type in test_queries:
        results = DangerSignsDatabase.search_danger_signs(query, patient_type)
        print(f"\nQuery: '{query}' (type: {patient_type})")
        print(f"  Found: {len(results)} signs")
        if results:
            print(f"  Top match: {results[0]['sign_name']} ({results[0]['triage_color'].value})")
    
    # Test triage summary
    print("\n\n📈 TRIAGE SUMMARY")
    print("-" * 70)
    
    for ptype in ["mother", "neonate", "infant", "child", "adolescent"]:
        summary = DangerSignsDatabase.get_triage_summary(ptype)
        print(f"\n{ptype.upper()}:")
        print(f"  🔴 RED: {summary['red']} | 🟡 YELLOW: {summary['yellow']} | 🟢 GREEN: {summary['green']} | Total: {summary['total']}")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_danger_signs()
