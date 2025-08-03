import json
import os
from typing import Dict, List, Optional, Tuple

class ReferenceRangeService:
    """Tıbbi referans aralıkları servisi"""
    
    def __init__(self):
        self.reference_data = self._load_reference_data()
    
    def _load_reference_data(self) -> Dict:
        """Referans aralıkları verisini yükler"""
        try:
            file_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 'data', 'medical_reference_ranges.json'
            )
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Referans aralıkları yüklenemedi: {e}")
            return {}
    
    def get_test_reference_range(self, test_name: str, age: int, gender: str = None) -> Optional[Dict]:
        """
        Test için referans aralığını getirir
        
        Args:
            test_name: Test adı (örn: 'glucose_fasting', 'hemoglobin')
            age: Hasta yaşı
            gender: Hasta cinsiyeti ('male', 'female')
        
        Returns:
            Referans aralığı bilgisi
        """
        try:
            # Test adını normalize et
            test_name = test_name.lower().replace(' ', '_')
            
            # Tüm kategorilerde test ara
            for category, category_data in self.reference_data.get('blood_tests', {}).items():
                if test_name in category_data.get('tests', {}):
                    test_data = category_data['tests'][test_name]
                    
                    # Yaş grubunu belirle
                    age_group = self._get_age_group(age)
                    
                    # Referans aralığını bul
                    reference_ranges = test_data.get('reference_ranges', {})
                    
                    # Cinsiyet ve yaş grubuna göre aralık seç
                    if gender and gender in reference_ranges:
                        if age_group in reference_ranges[gender]:
                            range_data = reference_ranges[gender][age_group]
                        else:
                            range_data = reference_ranges[gender]
                    elif age_group in reference_ranges:
                        range_data = reference_ranges[age_group]
                    elif 'adult' in reference_ranges:
                        range_data = reference_ranges['adult']
                    else:
                        # İlk mevcut aralığı al
                        range_data = next(iter(reference_ranges.values()))
                    
                    return {
                        'test_name': test_data['name'],
                        'unit': test_data['unit'],
                        'reference_range': range_data,
                        'critical_low': test_data.get('critical_low'),
                        'critical_high': test_data.get('critical_high'),
                        'description': test_data.get('description', ''),
                        'category': category_data['category']
                    }
            
            print(f"Test referans aralığı bulunamadı: {test_name}")
            return None
            
        except Exception as e:
            print(f"Referans aralığı getirme hatası: {e}")
            return None
    
    def evaluate_test_result(self, test_name: str, value: float, age: int, gender: str = None) -> Dict:
        """
        Test sonucunu değerlendirir
        
        Args:
            test_name: Test adı
            value: Test değeri
            age: Hasta yaşı
            gender: Hasta cinsiyeti
        
        Returns:
            Değerlendirme sonucu
        """
        try:
            reference_data = self.get_test_reference_range(test_name, age, gender)
            
            if not reference_data:
                return {
                    'status': 'unknown',
                    'message': 'Referans aralığı bulunamadı',
                    'value': value
                }
            
            min_val = reference_data['reference_range']['min']
            max_val = reference_data['reference_range']['max']
            critical_low = reference_data.get('critical_low')
            critical_high = reference_data.get('critical_high')
            
            # Durumu belirle
            if critical_low is not None and value <= critical_low:
                status = 'critical_low'
                risk_level = 'critical'
            elif critical_high is not None and value >= critical_high:
                status = 'critical_high'
                risk_level = 'critical'
            elif value < min_val:
                status = 'low'
                risk_level = 'high'
            elif value > max_val:
                status = 'high'
                risk_level = 'high'
            else:
                status = 'normal'
                risk_level = 'normal'
            
            # Risk seviyesi rengini al
            risk_color = self.reference_data.get('risk_levels', {}).get(risk_level, {}).get('color', 'gray')
            
            return {
                'status': status,
                'risk_level': risk_level,
                'risk_color': risk_color,
                'value': value,
                'unit': reference_data['unit'],
                'reference_range': f"{min_val} - {max_val}",
                'reference_min': min_val,
                'reference_max': max_val,
                'critical_low': critical_low,
                'critical_high': critical_high,
                'test_name': reference_data['test_name'],
                'category': reference_data['category'],
                'description': reference_data['description'],
                'message': self._get_status_message(status, value, min_val, max_val)
            }
            
        except Exception as e:
            print(f"Test sonucu değerlendirme hatası: {e}")
            return {
                'status': 'error',
                'message': 'Değerlendirme sırasında hata oluştu',
                'value': value
            }
    
    def _get_age_group(self, age: int) -> str:
        """Yaşa göre yaş grubunu belirler"""
        age_groups = self.reference_data.get('age_groups', {})
        
        for group_name, group_range in age_groups.items():
            if group_range['min'] <= age <= group_range['max']:
                return group_name
        
        return 'adult'  # Varsayılan
    
    def _get_status_message(self, status: str, value: float, min_val: float, max_val: float) -> str:
        """Duruma göre mesaj oluşturur"""
        if status == 'normal':
            return f"Değer normal aralıkta ({min_val} - {max_val})"
        elif status == 'low':
            return f"Değer normal aralığın altında (Normal: {min_val} - {max_val})"
        elif status == 'high':
            return f"Değer normal aralığın üstünde (Normal: {min_val} - {max_val})"
        elif status == 'critical_low':
            return f"Değer kritik seviyenin altında!"
        elif status == 'critical_high':
            return f"Değer kritik seviyenin üstünde!"
        else:
            return "Değer değerlendirilemedi"
    
    def get_all_tests(self) -> List[Dict]:
        """Tüm testleri listeler"""
        tests = []
        for category, category_data in self.reference_data.get('blood_tests', {}).items():
            for test_key, test_data in category_data.get('tests', {}).items():
                tests.append({
                    'key': test_key,
                    'name': test_data['name'],
                    'category': category_data['category'],
                    'unit': test_data['unit']
                })
        return tests
    
    def get_tests_by_category(self, category: str) -> List[Dict]:
        """Kategoriye göre testleri listeler"""
        category_data = self.reference_data.get('blood_tests', {}).get(category, {})
        tests = []
        for test_key, test_data in category_data.get('tests', {}).items():
            tests.append({
                'key': test_key,
                'name': test_data['name'],
                'unit': test_data['unit']
            })
        return tests
    
    def validate_test_name(self, test_name: str) -> bool:
        """Test adının geçerli olup olmadığını kontrol eder"""
        test_name = test_name.lower().replace(' ', '_')
        for category_data in self.reference_data.get('blood_tests', {}).values():
            if test_name in category_data.get('tests', {}):
                return True
        return False

# Global servis instance
reference_range_service = ReferenceRangeService() 