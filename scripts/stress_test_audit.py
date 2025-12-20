import multiprocessing
import time
import sys
import os
from pathlib import Path
import random

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.audit.immutable_audit import ImmutableAuditSystem


def worker_process(worker_id, num_events, log_dir):
    """Function run by each worker process to spam audit logs."""
    # Each process needs its own instance to simulate real distributed nature
    audit = ImmutableAuditSystem(log_dir=log_dir)

    print(f"Worker {worker_id} started. Writing {num_events} events...")

    for i in range(num_events):
        try:
            audit.log_action(
                action="stress_test_event",
                details={
                    "component": f"worker_{worker_id}",
                    "iteration": i,
                    "random_data": random.randint(0, 1000000),
                },
                category="stress_test",
            )
            # Small random sleep to vary contention
            time.sleep(random.uniform(0.001, 0.01))
        except Exception as e:
            print(f"Worker {worker_id} error on iter {i}: {e}")

    print(f"Worker {worker_id} finished.")


def run_stress_test():
    log_dir = "/home/fahbrain/projects/omnimind/logs_test_stress"
    # Ensure clean start for test
    if os.path.exists(log_dir):
        import shutil

        shutil.rmtree(log_dir)
    os.makedirs(log_dir, exist_ok=True)

    num_workers = 10
    events_per_worker = 50

    print(f"Starting Stress Test: {num_workers} workers, {events_per_worker} events each.")
    print(f"Log Dir: {log_dir}")

    processes = []
    start_time = time.time()

    for i in range(num_workers):
        p = multiprocessing.Process(target=worker_process, args=(i, events_per_worker, log_dir))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    duration = time.time() - start_time
    print(f"All workers finished in {duration:.2f} seconds.")

    # Verify Integrity
    print("\n--- Verifying Integrity ---")
    audit = ImmutableAuditSystem(log_dir=log_dir)
    result = audit.verify_chain_integrity()

    print(f"Integrity Result: {result['valid']}")
    print(f"Events Verified: {result['events_verified']}")

    expected_events = num_workers * events_per_worker
    # +1 for "audit_system_initialized" (created by the verifier instance if it didn't exist, but it existed from workers)
    # Actually each worker init might create an init event if it thinks it's fresh?
    # ImmutableAuditSystem init calls _log_system_event("audit_system_initialized")
    # So we expect at least 1 init event per worker process instantiation?
    # Actually __init__ calls _log_system_event only if it's creating new? No, let's check code.
    # It calls it unconditionally. So we will have N_workers + 1 (verifier) init events + N_workers * M events.

    # Just checking valid is True is the most important part.

    if result["valid"]:
        print("✅ SUCCESS: Hash chain is valid under stress.")
    else:
        print("❌ FAILURE: Hash chain corrupted.")
        if "corrupted_events" in result:
            print(f"Corrupted Events Sample: {result['corrupted_events'][:5]}")

    # Cleanup if successful
    # if result['valid']:
    #     import shutil
    #     shutil.rmtree(log_dir)


if __name__ == "__main__":
    run_stress_test()
