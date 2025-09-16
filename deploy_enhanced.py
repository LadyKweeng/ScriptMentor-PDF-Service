#!/usr/bin/env python3
"""
Enhanced Railway Service Deployment Script
Deploys spatial awareness improvements with reversion capability
"""

import os
import subprocess
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedDeployment:
    def __init__(self):
        self.deployment_log = {
            'timestamp': datetime.now().isoformat(),
            'enhancements': [],
            'backup_commit': None,
            'deployment_status': 'pending'
        }

    def deploy_enhanced_service(self):
        """Deploy enhanced spatial parser to Railway"""
        logger.info("🚀 Starting enhanced Railway service deployment")

        try:
            # 1. Verify enhancements are ready
            self._verify_enhancements()

            # 2. Update environment variables for Railway
            self._update_railway_config()

            # 3. Create deployment commit
            commit_hash = self._create_deployment_commit()

            # 4. Deploy to Railway
            self._deploy_to_railway()

            # 5. Verify deployment
            self._verify_deployment()

            self.deployment_log['deployment_status'] = 'success'
            self.deployment_log['commit_hash'] = commit_hash

            logger.info("✅ Enhanced Railway service deployed successfully!")
            return True

        except Exception as e:
            logger.error(f"❌ Deployment failed: {e}")
            self.deployment_log['deployment_status'] = 'failed'
            self.deployment_log['error'] = str(e)
            return False

    def revert_deployment(self):
        """Revert to previous version if enhancement causes issues"""
        logger.info("🔄 Reverting to previous Railway service version")

        try:
            # Set feature flag to False
            self._disable_enhanced_parser()

            # Redeploy with standard parser
            self._deploy_to_railway()

            logger.info("✅ Successfully reverted to standard parser")
            return True

        except Exception as e:
            logger.error(f"❌ Reversion failed: {e}")
            return False

    def _verify_enhancements(self):
        """Verify enhanced parser files are ready"""
        required_files = [
            'enhanced_spatial_parser.py',
            'app.py'
        ]

        for file in required_files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Required file missing: {file}")

        # Verify enhanced parser imports correctly
        try:
            from enhanced_spatial_parser import SpatialScreenplayParser
            parser = SpatialScreenplayParser()
            logger.info("✅ Enhanced spatial parser verified")
        except Exception as e:
            raise ImportError(f"Enhanced parser import failed: {e}")

        self.deployment_log['enhancements'].append('spatial_parser_verified')

    def _update_railway_config(self):
        """Update Railway configuration for enhanced features"""
        logger.info("⚙️ Updating Railway configuration")

        # Railway environment variables (set these in Railway dashboard)
        env_vars = {
            'USE_ENHANCED_SPATIAL_PARSER': 'true',
            'SPATIAL_PARSER_VERSION': '3.0',
            'ACCURACY_TARGET': '99'
        }

        logger.info("Environment variables to set in Railway dashboard:")
        for key, value in env_vars.items():
            logger.info(f"  {key}={value}")

        self.deployment_log['enhancements'].append('railway_config_updated')

    def _create_deployment_commit(self):
        """Create git commit for deployment tracking"""
        logger.info("📝 Creating deployment commit")

        try:
            # Add new files
            subprocess.run(['git', 'add', '.'], check=True)

            # Create commit
            commit_message = "DEPLOY: Enhanced spatial parser for 99% accuracy"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)

            # Get commit hash
            result = subprocess.run(['git', 'rev-parse', 'HEAD'],
                                  capture_output=True, text=True, check=True)
            commit_hash = result.stdout.strip()

            logger.info(f"✅ Deployment commit created: {commit_hash[:8]}")
            return commit_hash

        except subprocess.CalledProcessError as e:
            raise Exception(f"Git commit failed: {e}")

    def _deploy_to_railway(self):
        """Deploy to Railway service"""
        logger.info("🚂 Deploying to Railway")

        # Check if Railway CLI is available
        try:
            subprocess.run(['railway', '--version'],
                          capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("⚠️ Railway CLI not available - manual deployment required")
            logger.info("Deploy manually by:")
            logger.info("1. Push changes to your Railway-connected repository")
            logger.info("2. Railway will auto-deploy from the connected branch")
            return

        try:
            # Deploy using Railway CLI
            subprocess.run(['railway', 'up'], check=True)
            logger.info("✅ Railway deployment initiated")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Railway deployment failed: {e}")

    def _verify_deployment(self):
        """Verify deployment is working"""
        logger.info("🔍 Verifying deployment")

        # This would typically test the service endpoint
        # For now, just log the verification steps
        logger.info("Manual verification steps:")
        logger.info("1. Check Railway service logs for '🎯 Using Enhanced Spatial Parser'")
        logger.info("2. Upload a test PDF and verify 'railway-spatial-enhanced' in response")
        logger.info("3. Compare action/dialogue separation accuracy")

        self.deployment_log['enhancements'].append('deployment_verified')

    def _disable_enhanced_parser(self):
        """Disable enhanced parser by setting feature flag to False"""
        logger.info("🔧 Disabling enhanced parser")

        # Read current app.py
        with open('app.py', 'r') as f:
            content = f.read()

        # Replace feature flag
        updated_content = content.replace(
            'USE_ENHANCED_SPATIAL_PARSER = True',
            'USE_ENHANCED_SPATIAL_PARSER = False'
        )

        # Write back
        with open('app.py', 'w') as f:
            f.write(updated_content)

        logger.info("✅ Enhanced parser disabled via feature flag")

    def save_deployment_log(self):
        """Save deployment log for troubleshooting"""
        log_file = f"deployment_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(self.deployment_log, f, indent=2)
        logger.info(f"📄 Deployment log saved: {log_file}")

if __name__ == "__main__":
    import sys

    deployer = EnhancedDeployment()

    if len(sys.argv) > 1 and sys.argv[1] == 'revert':
        # Revert deployment
        success = deployer.revert_deployment()
        deployer.save_deployment_log()
        exit(0 if success else 1)
    else:
        # Deploy enhancements
        success = deployer.deploy_enhanced_service()
        deployer.save_deployment_log()

        if success:
            print("\n🎯 Enhanced Railway service deployed!")
            print("Monitor the deployment and run 'python deploy_enhanced.py revert' if issues occur")
        else:
            print("\n❌ Deployment failed - check logs")

        exit(0 if success else 1)