#!/usr/bin/env python3
"""Test script to verify namespace is correctly applied to all image types"""

from swebench.harness.test_spec.test_spec import make_test_spec

# Create a test instance
test_instance = {
    "instance_id": "apache__druid-13704",
    "repo": "apache/druid",
    "version": "0.22",
    "base_commit": "abc123",
    "test_patch": "test",
    "PASS_TO_PASS": [],
    "FAIL_TO_PASS": [],
}

# Test with namespace
namespace = "mirrors.tencent.com/hunyuan_yanguan"
spec = make_test_spec(test_instance, namespace=namespace)

print("=" * 80)
print("Testing namespace application to all image types")
print("=" * 80)
print(f"\nNamespace: {namespace}")
print(f"Is Remote Image: {spec.is_remote_image}")
print(f"\n1. Base Image Key:")
print(f"   {spec.base_image_key}")
print(f"\n2. Environment Image Key:")
print(f"   {spec.env_image_key}")
print(f"\n3. Instance Image Key:")
print(f"   {spec.instance_image_key}")
print("\n" + "=" * 80)

# Verify all images have the namespace prefix
has_namespace = all([
    namespace in spec.base_image_key,
    namespace in spec.env_image_key,
    namespace in spec.instance_image_key,
])

if has_namespace:
    print("✅ SUCCESS: All images have the correct namespace prefix!")
else:
    print("❌ FAILED: Some images are missing the namespace prefix!")
    if namespace not in spec.base_image_key:
        print(f"   - Base image missing namespace")
    if namespace not in spec.env_image_key:
        print(f"   - Environment image missing namespace")
    if namespace not in spec.instance_image_key:
        print(f"   - Instance image missing namespace")

print("=" * 80)
